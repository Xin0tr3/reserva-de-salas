from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from icalendar import Calendar, Event

def EnviarEmailConfirmacion (reserva):

    dominio = "http://127.0.0.1:8000"

    confirm_url = reverse('web-gestionar-reserva', kwargs = {'codigo': reserva.codigo, 'accion': 'confirmada'})
    cancel_url = reverse('web-gestionar-reserva', kwargs={'codigo' : reserva.codigo, 'accion': 'cancelada'})

    asunto = (f"Reserva de sala {reserva.codigo} - Pendiente de confirmacion")
    mensaje = (
        f"Hola {reserva.nombre_reservante},\n\n"
        f"Tu solicitud de reserva para la sala {reserva.sala_reservada} "
        f"el día {reserva.hora_inicio.strftime('%Y-%m-%d')} de {reserva.hora_inicio.strftime('%H:%M')} a {reserva.hora_termino.strftime('%H:%M')} ha sido registrada.\n\n"
        f"Por favor, confírmela o cancélala haciendo clic en los enlaces:\n\n"
        f"CONFIRMAR: {dominio}{confirm_url}\n"
        f"CANCELAR: {dominio}{cancel_url}\n\n"
        f"¡Gracias!"
    )

    calendario = ImportarCalendarioICalendar(reserva)


    email = EmailMessage(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [reserva.email],
    )

    email.attach('tu-reserva.ics', calendario, 'text/calendar')

    email.send(fail_silently=False)

def ImportarCalendarioICalendar(reserva):

    cal = Calendar()
    cal.add('prodid', '-//Servicio de reservas UTEM//utem.cl//')
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME', 'Reservas de Salas UTEM')
    event = Event()

    event.add('summary', reserva.nombre_evento)
    event.add('description', reserva.descripcion_evento)
    event.add('dtstart', reserva.hora_inicio)
    event.add('dtend', reserva.hora_termino)
    event.add('location', str(reserva.sala_reservada))
    event.add('uid', f'reserva-{reserva.codigo}@{settings.EMAIL_HOST_USER}')

    cal.add_component(event)

    return cal.to_ical()