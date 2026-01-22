from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render, redirect
from .models import Reservas, Invitados
from .forms import ReservaForm, InvitadosFormSet
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request,usuario)
            return redirect('admin-inicio')
        else:
            mensaje_error = "Usuario o contraseña incorrectos."
            return render(request, 'reservas/inicio_sesion.html', {'error_message': mensaje_error})
    return render(request, 'reservas/inicio_sesion.html')
            

def gestionar_reserva(request, codigo, accion):

    reserva = get_object_or_404(Reservas, codigo=codigo)

    if accion.lower() == 'confirmada':
        reserva.estado_reserva = 'CONFIRMADA'
        mensaje = "Reserva confirmada exitosamente"

    elif accion.lower() == 'cancelada':
        reserva.estado_reserva = 'CANCELADA'
        mensaje = "Reserva cancelada con exito"

    else :
        return HttpResponse("Accion no valida", status=400)
    
    reserva.save()

    context = {'reserva': reserva, 'mensaje': mensaje}
    return render(request, 'reservas/gestion_exitosa.html', context)

def agregar_invitados(request, reserva_id):
    reserva = Reservas.objects.get(id=reserva_id)
    capacidad_max = reserva.sala_reservada.capacidad_maxima
    contador = Invitados.objects.filter(codigo_reserva=reserva).count()

    if contador >= capacidad_max:
        return HttpResponse ("Error: Se a alcanzado la capacidad maxima de la sala")
    
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        formset = InvitadosFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # 1. Guardamos la reserva (pero no en la DB aún con commit=False)
            reserva = form.save()
            
            # 2. Le pasamos la reserva recién creada al formset
            formset.instance = reserva
            formset.save()
            
            return redirect('exito')
    else:
        form = ReservaForm()
        formset = InvitadosFormSet()

    return render(request, 'reserva_form.html', {
        'form': form,
        'invitados_formset': formset
    })