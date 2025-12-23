import os.path
import logging
from celery import shared_task
from .models import Reservas
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
logger = logging.getLogger(__name__)

@shared_task
def CalendarioGoogleReservas(reservas_id):
    try:
        reserva = Reservas.objects.get(id=reservas_id)
        print(f"Sincronizando reserva {reserva.codigo} en Google Calendar")
        return True

    except Reservas.DoesNotExist:
        return False
    
# 1. Helper de Autenticación
def obtener_servicio_google():
    # Lógica de credentials.json y token.json
    credenciales = None

    if os.path.exists("token.json"):
        credenciales = Credentials.from_authorized_user_file("token.json",SCOPES)

    if not credenciales or not credenciales.valid:
        if credenciales and credenciales.expired and credenciales.refresh_token:
            credenciales.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            credenciales = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credenciales.to_json())
    try:
        service = build("calendar", "v3", credentials=credenciales)
    except HttpError as error:
        print(f"Ocurrio un error: {error}")
    return service

# 2. Helper de Formateo
def formatear_reserva_a_evento_google(reserva):
    # Lógica de datetime a ISO 8601
    hora_inicio_calendario = reserva.hora_inicio
    hora_termino_calendario = reserva.hora_termino

    hora_i_isoformat = hora_inicio_calendario.isoformat()
    hora_t_isoformat = hora_termino_calendario.isoformat()
    return { 'summary': reserva.nombre_evento,
             'description':reserva.descripcion_evento,
             'location': reserva.sala_reservada.nombre_sala,
             'start':{
                'dateTime': hora_i_isoformat,
                'timeZone': 'America/Santiago',
             }, 
             'end':{ 
                'dateTime': hora_t_isoformat,
                'timeZone': 'America/Santiago',
             },
             'attendees' : [{'email': reserva.email}],
            }

# 3. LA TAREA (El punto de entrada)
@shared_task(autoretry_for=(HttpError, Exception))
def Registrar_en_google_calendar_task(reserva_id):
    # Coordina todo:
    # service = obtener_servicio_google()
    # evento = formatear_reserva_a_evento_google(reserva)
    # Enviar a Google...
    try:
        reserva = Reservas.objects.get(id=reserva_id)
    except Reservas.DoesNotExist:
        logger.error(f"id no encontrado")
        return 
    
    service = obtener_servicio_google()
    if service:
        evento = formatear_reserva_a_evento_google(reserva)

        evento_final = service.events().insert(calendarId='primary', body=evento).execute()
        logger.info(f"Evento creado: {evento_final.get('htmlLink')}")
    else:
        logger.error(f"El servicio no existe")
        raise Exception("Error en el servicio, reintentar.")