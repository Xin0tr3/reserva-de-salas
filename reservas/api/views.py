from ..models import Salas, Reservas, Invitados
from django.contrib.auth.models import User
from .serializers import SalaSerializer, ReservaSerializer, UserSerializer
from ..emails import ImportarCalendarioICalendar
from datetime import datetime
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from openpyxl import Workbook

class UserListaAdminAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')

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
        Q(estado_reserva='CONFIRMADA') | Q(estado_reserva='PENDIENTE')
        ).filter(
        Q(hora_inicio__lt = termino_solicitado) & Q(hora_termino__gt = inicio_solicitado)
        ).values_list('sala_reservada_id', flat=True)

        salas_disponibles = Salas.objects.exclude(id__in=reservas_solapadas)

        return salas_disponibles

class SalasCreacionAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SalaSerializer
    queryset = Salas.objects.all().order_by('nombre_sala')

class SalasModificacionELiminacionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SalaSerializer
    queryset = Salas.objects.all()
    lookup_field = 'pk'

class ReservaCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class=ReservaSerializer
    queryset = Reservas.objects.all()

class ReservaRetrieveDeleteAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReservaSerializer
    queryset = Reservas.objects.all()
    lookup_field = 'codigo'

class ReservaListaAdminAPIView(generics.ListAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Reservas.objects.all().order_by('-hora_inicio')

class ReservaDetallesAdminAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReservaSerializer
    queryset=Reservas.objects.all()
    lookup_field = 'codigo'

class ExportarInvitadosAPIView(APIView):
    """
    Endpoint para que el administrador descargue la lista de invitados en Excel.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, reserva_id):
        # 1. Obtenemos la reserva o lanzamos 404 si no existe
        reserva = get_object_or_404(Reservas, id=reserva_id)
        
        # 2. Filtramos los invitados asociados a esa reserva
        invitados_r = Invitados.objects.filter(codigo_reserva=reserva)

        # 3. Inicializamos el libro de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Lista de Invitados"

        # 4. Definimos y agregamos los encabezados
        header = ['Nombre Invitado', 'Apellidos Invitados', 'Rol', 'Carrera', 'Facultad', 'Sexo', 'Código Reserva']
        ws.append(['Invitados del evento: ', reserva.nombre_evento])
        ws.append(['Sala: ', reserva.sala_reservada.nombre_sala])
        ws.append([]) # Espacio visual
        ws.append(header)

        # 5. Agregamos los datos de cada invitado
        for invitado in invitados_r:
            ws.append([
                invitado.nombre_invitado,
                invitado.apellidos_invitado,
                invitado.get_rol_display(), # Muestra el texto legible del Choice
                invitado.carrera,
                invitado.facultad,
                invitado.get_sexo_display(),
                reserva.codigo # El código único de la reserva
            ])

        # 6. Preparamos la respuesta HTTP para descargar el archivo .xlsx
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="invitados_{reserva.codigo}.xlsx"'

        wb.save(response)
        return response

class DescargarCalendarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo):
        reserva = get_object_or_404(Reservas, codigo=codigo)
        calendario = ImportarCalendarioICalendar(reserva)

        response = HttpResponse(calendario, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="reserva_{codigo}.ics"'
        return response