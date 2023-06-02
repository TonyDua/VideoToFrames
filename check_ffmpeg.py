import os
import requests
import shutil
import subprocess
import zipfile

def check_ffmpeg():
    # Check if FFmpeg is installed
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except FileNotFoundError:
        # FFmpeg is not installed, download and install it
        print('FFmpeg is not installed, downloading...')
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        response = requests.get(url)
        with open('ffmpeg.zip', 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove('ffmpeg.zip')
        print('FFmpeg has been downloaded and extracted.')
        # Add FFmpeg to system PATH
        ffmpeg_path = os.path.abspath('ffmpeg-4.4-essentials_build/bin')
        if 'ffmpeg' not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + ffmpeg_path
        print('FFmpeg has been added to system PATH.')

print(os.environ['PATH'])