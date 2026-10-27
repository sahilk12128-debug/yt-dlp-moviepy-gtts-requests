import os
import subprocess
import requests

# आपकी Facebook Page ID और GitHub Secrets से Access Token अपने आप आ जाएगा
FACEBOOK_PAGE_ID = "1322066784333919"
FACEBOOK_ACCESS_TOKEN = os.environ.get(EAAQcE9ZBE5XcBS6HRFwmBle5RhzSAmAwZA49ZAevdXm72zeqD3ldiKpbB4ZBu0FvnTZCiCRsWRINlwj2lI74NU3RxatTr9VNaCnx0bs1esSqZAlZAZCU35zFr1dV5APJxm5ofQwbZBIufeoeTt2c3vShX5Agiv32ScZAO2zgsiXgVc45TfWAEjFvVuHuqWTrgUXWzdkmZCA)
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"

def download_and_process_video():
    print("Step 1: Downloading video via direct source...")
    video_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
    
    try:
        response = requests.get(video_url, stream=True)
        with open(RAW_VIDEO, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("✅ Raw video downloaded successfully.")
        
        print("Step 2: Processing video using FFmpeg...")
        ffmpeg_command = [
            'ffmpeg', '-y', '-i', RAW_VIDEO,
            '-vf', "eq=brightness=0.03:saturation=1.1",
            '-t', '30',
            VIDEO_PATH
        ]
        
        subprocess.run(ffmpeg_command, check=True)
        print("✅ Video processed and edited successfully as 'reel.mp4'.")
        
    except Exception as e:
        print(f"❌ Error during download/processing: {str(e)}")
        raise e

def upload_to_facebook():
    print("Step 3: Starting Facebook Reel Upload process...")

    if not FACEBOOK_ACCESS_TOKEN:
        print("❌ Error: FACEBOOK_ACCESS_TOKEN is missing in GitHub Secrets!")
        return

    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Processed video file '{VIDEO_PATH}' not found!")
        return

    try:
        # Step 4: Start the Reel Upload Session using 'START' phase
        print("Step 4: Starting video upload session with Facebook...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {
            'upload_phase': 'START',
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        
        response_raw = requests.post(url, data=payload)
        print(f"Facebook Raw Response: {response_raw.text}")
        
        response = response_raw.json()
        
        if 'video_id' not in response or 'upload_url' not in response:
            print(f"❌ Facebook Start Failed: {response}")
            return
            
        video_id = response['video_id']
        upload_url = response['upload_url']
        print(f"✅ Start successful! Video ID: {video_id}")

        # Step 5: Upload the Video Binary
        print("Step 5: Uploading video binary data to Facebook...")
        with open(VIDEO_PATH, 'rb') as video_file:
            video_bytes = video_file.read()
            
        headers = {
            'Authorization': f'OAuth {FACEBOOK_ACCESS_TOKEN}',
            'offset': '0',
            'file_size': str(len(video_bytes))
        }
        
        upload_response = requests.post(upload_url, headers=headers, data=video_bytes).json()
        print(f"Upload Binary Response: {upload_response}")
        print("✅ Video binary uploaded successfully.")

        # Step 6: Finish/Publish the Reel using 'FINISH' phase
        print("Step 6: Publishing the Reel on Facebook...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            'upload_phase': 'FINISH',
            'video_state': 'PUBLISHED',
            'description': 'Automated Daily Movie Short Reel #shorts #viral',
            'video_id': video_id,
            'access_token': FACEBOOK_ACCESS_TOKEN
        
        publish_response = requests.post(publish_url, data=publish_payload).json()
        print(f"Publish Response: {publish_response}")
        
        if publish_response.get('success'):
            print("🎉 Success! Facebook Reel published successfully.")
        else:
            print(f"⚠️ Warning/Error during publish: {publish_response}")

    except Exception as e:
        print(f"❌ An exception occurred during upload: {str(e)}")

if __name__ == "__main__":
    download_and_process_video()
    upload_to_facebook()
