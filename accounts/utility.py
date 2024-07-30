from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
# from attrs import define

class GoogleRawLoginCredentials:
    client_id : str
    client_secret : str 
    project_id: str

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