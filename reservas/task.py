from celery import shared_task
from .models import Reservas

@shared_task
def CalendarioGoogleReservas(reservas_id):
    try:
        reserva = Reservas.objects.get(id=reservas_id)
        print(f"Sincronizando reserva {reserva.codigo} en Google Calendar")
        return True

    except Reservas.DoesNotExist:
        return False
