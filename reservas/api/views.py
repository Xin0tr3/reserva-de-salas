from ..models import Salas, Reservas
from .serializers import SalaSerializer, ReservaSerializer
from datetime import datetime
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

class SalaListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SalaSerializer
    queryset = Salas.objects.all()


    def get_queryset(self):

        fecha_str = self.request.query_params.get('fecha')
        hora_inicio_str = self.request.query_params.get('hora_inicio')
        hora_termino_str = self.request.query_params.get('hora_termino')

        if not all([fecha_str, hora_inicio_str, hora_termino_str]):
            return Salas.objects.all()
        
        try:
            inicio_solicitado = datetime.strptime(f"{fecha_str} {hora_inicio_str}", "%Y-%m-%d %H:%M")
            termino_solicitado = datetime.strptime(f"{fecha_str} {hora_termino_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return Salas.objects.none()
    
        reservas_solapadas = Reservas.objects.filter(
        Q(estado='CONFIRMADA') | Q(estado='PENDIENTE')
        ).filter(
        Q(hora_inicio__lt = termino_solicitado) & Q(hora_termino__gt = inicio_solicitado)
        ).values_list('sala_reservada_id', flat=True)

        salas_disponibles = Salas.objects.exclude(id__in=reservas_solapadas)

        return salas_disponibles