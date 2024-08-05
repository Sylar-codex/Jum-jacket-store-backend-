from django.core.mail import EmailMessage
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from attrs import define
from random import SystemRandom
from urllib.parse import urlencode
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
import jwt
from typing import Any, Dict
import requests

class Util :
    def send_email(data):
        email = EmailMessage(
            data['email_subject'],
            data['email_body'],
            settings.EMAIL_HOST_USER,
            [data['to_email']]
        )
        email.send(fail_silently=False)




@define
class GoogleRawLoginCredentials:
    client_id : str
    client_secret : str 
    project_id: str

@define
class GoogleAccessTokens :
    id_token : str
    access_token : str

    def decode_id_token(self) -> Dict[str, str] :
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature" : False})
        return decoded_token

def get_google_raw_login_credentials() -> GoogleRawLoginCredentials :
    client_id = settings.GOOGLE_PROJECT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    project_id = settings.GOOGLE_PROJECT_ID

    if not client_id :
        ImproperlyConfigured("GOOGLE_PROJECT_ID is missing")

    if not client_secret :
        ImproperlyConfigured("GOOGLE_CLIENT_SECRET is missing")

    if not project_id :
        ImproperlyConfigured("GOOGLE_PROJECT_ID is missing")
    
    credentials = GoogleRawLoginCredentials(
        client_id=client_id, 
        client_secret=client_secret,
        project_id=project_id
        )
    return credentials

class GoogleRawLoginFlowService:
    API_URI = reverse_lazy("google-login-callback")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]

    def __init__(self) :
        self.credentials = get_google_raw_login_credentials()
        

    @staticmethod
    def _generate_state_session_token(length=30, chars= UNICODE_ASCII_CHARACTER_SET) :
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self) :
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f'{domain}{api_uri}'
        return redirect_uri

    def get_authorization_url(self) :
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type":"code",
            "client_id" : self._credentials.client_id,
            "redirect_uri":redirect_uri,
            "scope":" ".join(self.SCOPES),
            "state":state,
            "access_type":"offline",
            "include_granted_scopes":"true",
            "prompt":"select_account"
        }

        query_params = urlencode(params)
        authorization_url = f'{self.GOOGLE_AUTH_URL}?{query_params}'
        return authorization_url, state
    
    def get_tokens(self, *, code:str) -> GoogleAccessTokens:

        redirect_uri = self._get_redirect_uri()
        
        data = {
            "code": code,
            "client_id":self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri" : redirect_uri,
            "giant_type":"authorization_code"
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok :
            raise "Failed to obtain access token from google"
        
        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token= tokens["id_token"],
            access_token=tokens["access_token"]
        )

        return google_tokens
    


 