import requests


def fetch_and_process_transcript(video_id):
    url = "https://tactiq-apps-prod.tactiq.io/transcript"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"videoUrl": f"https://www.youtube.com/watch?v={video_id}"},
    )
    if response.status_code == 200:
        json_data = response.json()
        scripts = ""
        for item in json_data.get("captions", []):
            if item.get("text") is not None and item.get("text", "") != "No text":
                scripts += item.get("text", "")
        return scripts
    return None
