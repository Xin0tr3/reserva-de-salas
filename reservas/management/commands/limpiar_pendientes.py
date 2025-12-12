from django.core.management.base import BaseCommand
from django.utils import timezone
from reservas.models import Reservas

class Command(BaseCommand):

    def handle(self, *args, **opciones):

        now = timezone.now

        reservas_a_limpiar = Reservas.objects.filter(
            estado_reserva = 'PENDIENTE', 
            hora_inicio__lt = now
            )

        count = reservas_a_limpiar.count()

        if count > 0:
            reservas_a_limpiar.update(estado_reserva = 'CADUCADA')

            self.stdout.write(self.style.SUCCESS(
                f'{count} limpiadas con exito'
            ))
        
        else:
            self.stdout.write(self.style.SUCCESS(
                'No se encontraron registros por limpiar'
            ))
            




