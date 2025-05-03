import datetime
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi import HTTPException, APIRouter, Request

router = APIRouter()

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@router.get("/events/get")
async def get_google_calendar_events(request: Request):
    try:
        if 'user' not in request.session:
            raise HTTPException(status_code=401, detail="Não autenticado")

        access_token = request.session['user'].get('access_token')
        if not access_token:
            raise HTTPException(status_code=400, detail="Token de acesso não encontrado")

        creds = Credentials(token=access_token, scopes=SCOPES)
        service = build("calendar", "v3", credentials=creds)

        events_result = service.events().list(
            calendarId="primary",
            maxResults=50,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        return {"events": events_result.get('items', [])}

    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"Erro na API do Google: {str(error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/events/post")
async def save_google_calendar_events(request: Request):
    try:
        if 'user' not in request.session:
            raise HTTPException(status_code=401, detail="Não autenticado")

        access_token = request.session['user'].get('access_token')
        if not access_token:
            raise HTTPException(status_code=400, detail="Token de acesso não encontrado")

        creds = Credentials(
            token=access_token,
            scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        
        #Evento genério, Editar em caso de testes
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        created_event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return {
            "message": "Evento criado com sucesso!",
            "event_link": created_event.get('htmlLink')
        }

    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"Erro na API do Google: {str(error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

