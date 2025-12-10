from ..models import Salas, Reservas
from .serializers import SalaSerializer, ReservaSerializer
from datetime import datetime
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

class SalaDisponiblesAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
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

class SalasCreacionAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SalaSerializer
    queryset = Salas.objects.all().order_by('nombre')

class SalasModificacionELiminacionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SalaSerializer
    queryset = Salas.objects.all()
    lookup_field = 'pk'

class ReservaCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class=ReservaSerializer
    queryset = Reservas.objects.all()

class ReservaListaAdminAPIView(generics.ListAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Reservas.objects.all().order_by('-hora_inicio')

class ReservaDetallesAdminAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReservaSerializer
    queryset=Reservas.objects.all()
    lookup_field = 'codigo'

def gestionar_reserva(request, codigo, accion):

    reserva = get_object_or_404(Reservas, codigo=codigo)

    if accion.lower() == 'confirmada':
        reserva.estado_reserva = 'CONFIRMADA'
        mensaje = "Reserva confirmada exitosamente"

    elif accion.lower() == 'cancelada':
        reserva.estado_reserva = 'CANCELADA'
        mensaje = "Reserva cancelada con exito"

    else :
        return HttpResponse("Accion no valida", status=400)
    
    reserva.save()

    context = {'reserva': reserva, 'mensaje': mensaje}
    return render(request, 'reservas/gestion_exitosa.html', context)
