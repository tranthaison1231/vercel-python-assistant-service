import requests


def fetch_and_process_transcript(video_id):
    url = f"https://youtubenavigator.com/api/fetch-transcript?url=https://www.youtube.com/watch?v={video_id}&timestamps=true"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        scripts = ""
        for item in json_data.get("segments", {}):
            scripts += item.get("text", "")
        return scripts
    return None
