from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Reservas, Invitados

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

def invitados_excel(request, reserva_id):
    reserva = Reservas.objects.get(id=reserva_id)
    invitados_r = Invitados.objects.filter(codigo_reserva=reserva)

    wb = Workbook()
    ws = wb.active

    Header = ['Nombre Invitado', 'Apellidos Invitados', 'Rol', 'Carrera', 'Facultad', 'Sexo', 'Codigo Reserva']
    ws.append(['Invitados del evento: ', reserva.nombre_evento])
    ws.append(['Sala: ', reserva.sala_reservada.nombre_sala])
    ws.append([])
    ws.append(Header)

    for invitados in invitados_r:
        ws.append[
            invitados.nombre_invitado,
            invitados.apellidos_invitado,
            invitados.get_rol_display(),
            invitados.carrera,
            invitados.facultad,
            invitados.get_sexo_display(),
            invitados.codigo_reserva
        ]
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="invitados_{reserva.codigo}.xlsx"'

    wb.save(response)
    return response

def agregar_invitados(request, reserva_id):
    reserva = Reservas.objects.get(id=reserva_id)
    capacidad_max = reserva.sala_reservada.capacidad_maxima
    contador = Invitados.objects.filter(codigo_reserva=reserva).count()

    if contador >= capacidad_max:
        return HttpResponse ("Error: Se a alcanzado la capacidad maxima de la sala")