from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Reservas

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