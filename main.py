import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    
    # Temporary client config dictionary for OAuth flow
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }
    
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    print("YouTube Client Initialized Successfully!")

if __name__ == "__main__":
    get_authenticated_service()
