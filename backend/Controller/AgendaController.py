import datetime
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from backend.Dto.EventRequest import EventRequest, Reminders, ReminderOverride, Attendee, EventDateTime
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

@router.post("/events/post")
async def get_google_calendar_events(request: Request, event_request: EventRequest):
    try:
        if 'user' not in request.session and not event_request.access_token:
            raise HTTPException(status_code=401, detail="Não autenticado")

        access_token = (
            request.session['user'].get('access_token')
            if 'user' in request.session else event_request.access_token
        )

        if not access_token:
            raise HTTPException(status_code=400, detail="Token de acesso não encontrado")

        creds = Credentials(
            token=access_token,
            scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': event_request.summary,
            'location': event_request.location,
            'description': event_request.description,
            'start': {
                'dateTime': event_request.start.dateTime.isoformat(),
                'timeZone': event_request.start.timeZone,
            },
            'end': {
                'dateTime': event_request.end.dateTime.isoformat(),
                'timeZone': event_request.end.timeZone,
            },
            'attendees': [{'email': attendee.email} for attendee in event_request.attendees],
            'reminders': {
                'useDefault': event_request.reminders.useDefault if event_request.reminders else True,
                'overrides': [
                    {
                        'method': r.method,
                        'minutes': r.minutes
                    } for r in event_request.reminders.overrides
                ] if event_request.reminders and event_request.reminders.overrides else []
            }
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
