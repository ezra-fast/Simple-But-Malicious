# This script was contributed to by me, not designed.

import os
import requests
import json
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]+', '-', filename)

def fetch_traffic_camera_photos():
    url = 'https://data.calgary.ca/resource/k7p9-kppz.json'
    photo_directory = 'C:/temp/idk'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = json.loads(response.text)

        # Create the photo directory if it doesn't exist
        os.makedirs(photo_directory, exist_ok=True)

        # Download and save each photo
        for item in data:
            photo_url = item['camera_url']['url']
            photo_response = requests.get(photo_url)
            photo_response.raise_for_status()

            filename = f"Camera-{item['camera_url']['description']} - {item['quadrant']} - {item['camera_location']}.jpg"
            filename = sanitize_filename(filename)  # Sanitize the filename
            photo_path = os.path.join(photo_directory, filename)
            with open(photo_path, 'wb') as photo_file:
                photo_file.write(photo_response.content)

            print(f'Saved {photo_path}')

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

# Call the function to fetch traffic camera photos
fetch_traffic_camera_photos()
