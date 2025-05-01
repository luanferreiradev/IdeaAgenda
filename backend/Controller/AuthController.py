import os

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from backend.AuthConfig import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from dotenv import load_dotenv

router = APIRouter()
oauth = OAuth()
load_dotenv()

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/login/google")
async def login_with_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/login/google/callback")
async def auth_google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        if not token.get('id_token'):
            user_info = token.get('userinfo')
            if not user_info:
                user_info = await oauth.google.userinfo(request=request, token=token)
        else:
            user_info = await oauth.google.parse_id_token(request, token)

        return {"access_token": token, "user_info": user_info}
    except Exception as e:
        print(f"Error during Google OAuth callback: {str(e)}")
        return RedirectResponse(url="/")