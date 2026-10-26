import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import yt_dlp
from moviepy.editor import VideoFileClip

# YouTube API scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def download_and_prepare_video():
    print("Downloading video using yt-dlp...")
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'input_video.mp4',
        'max_filesize': 50000000, 
    }
    
    # यहाँ आप किसी भी वीडियो का लिंक दे सकते हैं जिसे शॉर्ट्स के रूप में डालना है
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=6hPY4RhR4Yk'])
    
    print("Editing video into a Short (9:16 format)...")
    clip = VideoFileClip("input_video.mp4")
    
    if clip.duration > 30:
        clip = clip.subclip(0, 30)
        
    w, h = clip.size
    target_width = int(h * (9/16))
    x_center = w / 2
    cropped_clip = clip.crop(x1=x_center - target_width/2, y1=0, x2=x_center + target_width/2, y2=h)
    final_clip = cropped_clip.resize((1080, 1920))
    
    final_clip.write_videofile("final_short.mp4", codec="libx264", audio_codec="aac")
    print("Video prepared successfully!")

def upload_to_youtube():
    print("Authenticating with YouTube API...")
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    
    # Refresh token से सीधे बिना बार-बार लॉगिन किए कनेक्शन बन जाएगा
    creds = google.oauth2.credentials.Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    print("Uploading video to YouTube...")
    body = {
        'snippet': {
            'title': 'Auto Uploaded Short #Shorts',
            'description': 'This video was uploaded automatically using GitHub Actions.',
            'tags': ['shorts', 'automation'],
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'public'  # या 'private' / 'unlisted' रख सकते हैं
        }
    }
    
    media = MediaFileUpload('final_short.mp4', chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")
            
    print(f"Video uploaded successfully! Video ID: {response.get('id')}")

if __name__ == "__main__":
    download_and_prepare_video()
    upload_to_youtube()
