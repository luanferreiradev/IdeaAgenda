import datetime
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi import HTTPException, APIRouter, Request

router = APIRouter()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@router.get("/events")
async def get_google_calendar_events(request: Request):
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

        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        return {"events": events_result.get('items', [])}

    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"Erro na API do Google: {str(error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")