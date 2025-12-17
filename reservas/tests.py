from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from reservas.api.serializers import ReservaSerializer
from reservas.models import Salas, Reservas

class ReservaSerializerTestCase(TestCase):
    def setUp(self):
        self.sala = Salas.objects.create(
            nombre_sala = 'Sala Prueba',
            capacidad_maxima = 10
        )

        now = timezone.now()
        self.hora_inicio_existente = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        self.hora_termino_existente = self.hora_inicial_existente + timedelta(hours=1)

        self.reserva_existente = Reservas.objects.create(
            sala_reservada=self.sala,
            nombre_reservante='Usuario Base',
            email='base@utem.cl',
            hora_inicio=self.hora_inicio_existente,
            hora_termino=self.hora_termino_existente,
            nombre_evento='Reunión de prueba',
            descripcion_evento='Reserva que ya existe en la DB',
            estado_reserva='CONFIRMADA',
        )

        self.valid_data = {
            'sala_reservada': self.sala.pk, 
            'nombre_reservante': 'Nuevo Solicitante',
            'email': 'nuevo@utem.cl',
            'nombre_evento': 'Nuevo Evento',
            'descripcion_evento': 'Descripción de la nueva reserva',
        }

    def testeo_reserva_sin_solapamiento_exito(self):
        nuevo_inicio = self.hora_inicio_existente - timedelta(hours=1)
        nuevo_termino = self.hora_inicio_existente

        data = self.valid_data.copy()
        data['hora_inicio'] = nuevo_inicio
        data['hora_termino'] = nuevo_termino

        serializer = ReservaSerializer(data=data)

        self.assertTrue(serializer.is_valid(), f"El Serializer falló: {serializer.errors}")

        reserva = serializer.save()
        self.assertIsInstance(reserva, Reservas)
        self.assertEqual(reserva.hora_inicio, nuevo_inicio)
        self.assertEqual(Reservas.objects.count(), 2)

    def testeo_reserva_solapamiento_fallo(self):
        nuevo_inicio = self.hora_inicio_existente + timedelta(minutes=30)
        nuevo_termino = self.hora_termino_existente - timedelta(minutes= 30)

        data = self.valid_data.copy()
        data['hora_inicio'] = nuevo_inicio
        data['hora_termino'] = nuevo_termino

        serializer = ReservaSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('Esta sala ya está reservada', str(serializer.errors))
        self.assertEqual(Reservas.objects.count(), 1)

    def testeo_reserva_solapamiento_inicio(self):
        nuevo_inicio = self.hora_inicio_existente - timedelta(minutes=30)
        nuevo_termino = self.hora_termino_existente + timedelta(minutes= 30)

        data = self.valid_data.copy()
        data['hora_inicio'] = nuevo_inicio
        data['hora_termino'] = nuevo_termino

        serializer = ReservaSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(Reservas.objects.count(), 1)

    def testeo_reserva_solapamiento_final(self):
        nuevo_inicio = self.hora_inicio_existente + timedelta(minutes=30)
        nuevo_termino = self.hora_termino_existente + timedelta(minutes= 30)

        data = self.valid_data.copy()
        data['hora_inicio'] = nuevo_inicio
        data['hora_termino'] = nuevo_termino

        serializer = ReservaSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(Reservas.objects.count(), 1)

    def testeo_reserva_solapamiento_toque(self):
        data_a = self.valid_data.copy()
        data_a['hora_inicio'] = self.hora_inicio_existente - timedelta(hours=1)
        data_a['hora_termino'] = self.hora_inicio_existente

        serializer_a = ReservaSerializer(data=data_a)
        self.assertTrue(serializer_a.is_valid(), "Fallo en el toque al inicio (09:00-10:00)")
        serializer_a.save()

        data_b = self.valid_data.copy()
        data_b['hora_inicio'] = self.hora_termino_existente
        data_b['hora_termino'] = self.hora_termino_existente  + timedelta(hours=1)

        serializer_b = ReservaSerializer(data=data_a)
        self.assertTrue(serializer_b.is_valid(), "Fallo en el toque al final (11:00-12:00)")
        serializer_b.save()

        self.assertEqual(Reservas.objects.count(), 3)