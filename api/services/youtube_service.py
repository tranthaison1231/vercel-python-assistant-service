import yt_dlp
import scrapetube

from api.utils.get_date_from_time_left import get_date_from_time_left


def get_latest_video_info(channel_url):
    ydl_opts = {
        "extract_flat": True,
        "playlistend": 1,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if info is None or "entries" not in info:
            return None
        latest_video = info["entries"][0]
        return {
            "title": latest_video["title"],
            "url": latest_video["url"],
            "video_id": latest_video["id"],
        }


def get_videos_info(channel_url, max_results=5):
    ydl_opts = {
        "extract_flat": True,
        "playlistend": 1,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if info is None or "entries" not in info:
            return None
        videos = scrapetube.get_channel(info["id"], limit=max_results)

        video_list = []
        for video in videos:
            video_id = video["videoId"]
            title = video["title"]["runs"][0]["text"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            published_text = video.get("publishedTimeText", {}).get("simpleText", "")
            channel_name = info["channel"]

            video_list.append(
                {
                    "title": title,
                    "url": url,
                    "published_date": get_date_from_time_left(
                        time_left_text=published_text, timezone="Asia/Ho_Chi_Minh"
                    ),
                    "channel": channel_name,
                    "video_id": video_id,
                }
            )

        return video_list


def get_streams_info(channel_url, max_results=5):
    ydl_opts = {
        "extract_flat": True,
        "playlistend": 1,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if info is None or "entries" not in info:
            return None
        videos = scrapetube.get_channel(
            info["id"], limit=max_results, content_type="streams"
        )
        channel_name = info["channel"]

        video_list = []
        for video in videos:
            video_id = video["videoId"]
            title = video["title"]["runs"][0]["text"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            published_text = video.get("publishedTimeText", {}).get("simpleText", "")
            published_text_split = published_text.split("Streamed")[1].strip()

            video_list.append(
                {
                    "title": title,
                    "url": url,
                    "published_date": get_date_from_time_left(
                        time_left_text=published_text_split, timezone="Asia/Ho_Chi_Minh"
                    ),
                    "channel": channel_name,
                    "video_id": video_id,
                }
            )

        return video_list
