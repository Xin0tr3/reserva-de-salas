from rest_framework import serializers
from ..models import Salas, Reservas
from django.db.models import Q
import secrets

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salas
        fields = ['__all__']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = ['__all__']

    def validate(self, data):
        if data['hora_inicio'] >=data['hora_termino']:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora de término.")
            
        reservas_solapadas = Reservas.objects.filter(
           Q(sala_reservada=data['sala_reservada']) & Q(estado_reserva__in=['CONFIRMADA', 'PENDIENTE'])
        ).filter(
            Q(hora_inicio__lt=data['hora_termino']) & Q(hora_termino__gt=data['hora_inicio'])
        ).values_list('id',flat=True)
        if reservas_solapadas.exists():
            raise serializers.ValidationError("La sala ya está resrvada en el horario solicitado.")
        return data
    
    def validar_rut(self, value):
        rut = value.replace(".", "").replace("-","")
        if len(rut) < 8 or len(rut) > 9:
            raise serializers.ValidationError("RUT inválido.")
        return value

    def create(self, validated_data):
        codigo_unico = secrets.token_urlsafe(16)
        validated_data['codigo']= codigo_unico

        return super().create(validated_data)