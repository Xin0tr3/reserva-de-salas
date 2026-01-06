from rest_framework import serializers
from ..models import Salas, Reservas, Invitados
from django.db.models import Q
from django.db import transaction
from ..emails import EnviarEmailConfirmacion
import secrets

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salas
        fields = '__all__'

class InvitadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitados
        # Se excluye codigo_reserva porque se asignará automaticamente en el create
        exclude = ['codigo_reserva']

class ReservaSerializer(serializers.ModelSerializer):

    invitados = InvitadoSerializer(many=True, required=False)

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
        
        invitados_data = data.get('invitados', [])
        if sala_reservada_actual and len(invitados_data) > sala_reservada_actual.capacidad_maxima:
            raise serializers.ValidationError(
                f"La sala '{sala_reservada_actual.nombre_sala}' solo permite {sala_reservada_actual.capacidad_maxima} personas. "
                f"Has intentado agregar {len(invitados_data)}."
            )

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
    
    def validate_rut(self, value):
        rut = value.replace(".", "").replace("-","")
        if len(rut) < 8 or len(rut) > 9:
            raise serializers.ValidationError("RUT inválido.")
        return value

    def create(self, validated_data):
        # Se separan los invitados de los datos de la reserva
        invitados_data = validated_data.pop('invitados', [])

        with transaction.atomic():
            # Se genera codigo
            validated_data['codigo'] = secrets.token_urlsafe(16)

            # Se crea la reserva
            reserva = Reservas.objects.create(**validated_data)

            #Se crean los invitados y se asocian a la reserva
            for invitado in invitados_data:
                    Invitados.objects.create(codigo_reserva=reserva, **invitado)
                    
        EnviarEmailConfirmacion(reserva)

        return reserva