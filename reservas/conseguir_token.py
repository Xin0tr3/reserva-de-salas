import os.path
import logging
from celery import shared_task
#from reservas.models import Reservas
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

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

obtener_servicio_google()