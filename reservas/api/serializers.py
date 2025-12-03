from rest_framework import serializers
from ..models import Salas, Reservas

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salas
        fields = ['__all__']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = ['__all__']