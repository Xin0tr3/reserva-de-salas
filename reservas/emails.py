from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

def EnviarEmailConfirmacion (reserva):

    dominio = "http://127.0.0.1:8000"

    confirm_url = reverse('web-gestionar-reserva', kwargs = {'codigo': reserva.codigo, 'accion': 'confirmar'})
    cancel_url = reverse('web-gestionar-reserva', kwargs={'codigo' : reserva.codigo, 'accion': 'cancelar'})

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

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FOR_EMAIL,
        [reserva.email],
        fail_silently=False,
    )