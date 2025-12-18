from rest_framework import serializers
from ..models import Salas, Reservas
from django.db.models import Q
from ..emails import EnviarEmailConfirmacion
from ..task import CalendarioGoogleReservas
import secrets

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salas
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = '__all__'

    def validate(self, data):
        hora_inicio = data.get('hora_inicio', self.instance.hora_inicio if self.instance else None)
        hora_termino = data.get('hora_termino', self.instance.hora_termino if self.instance else None)
        sala_reservada_actual = data.get('sala_reservada', self.instance.sala_reservada if self.instance else None)

        if hora_inicio and hora_termino:
            if hora_inicio >= hora_termino:
                raise serializers.ValidationError("La hora de inicio debe ser menor a la hora de término.")

        if hora_inicio and hora_termino and sala_reservada_actual: 
            reservas_solapadas = Reservas.objects.filter(
            Q(sala_reservada=sala_reservada_actual) & Q(estado_reserva__in=['CONFIRMADA', 'PENDIENTE'])
            ).filter(
                Q(hora_inicio__lt=hora_termino) & Q(hora_termino__gt=hora_inicio)
            ).values_list('id',flat=True)

            if self.instance:
                reservas_solapadas = reservas_solapadas.exclude(pk=self.instance.pk)

            if reservas_solapadas.exists():
                raise serializers.ValidationError("La sala ya está reservada en el horario solicitado.")
        return data
    
    def validar_rut(self, value):
        rut = value.replace(".", "").replace("-","")
        if len(rut) < 8 or len(rut) > 9:
            raise serializers.ValidationError("RUT inválido.")
        return value

    def create(self, validated_data):
        codigo_unico = secrets.token_urlsafe(16)
        validated_data['codigo']= codigo_unico

        reserva = super().create(validated_data)

        EnviarEmailConfirmacion(reserva)

        CalendarioGoogleReservas.delay(reserva.id)
        return reserva