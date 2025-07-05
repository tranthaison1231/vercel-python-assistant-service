from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Blueprint, request, jsonify
from api.services.transcript_service import fetch_and_process_transcript
from api.services.youtube_service import get_latest_video_info, get_streams_info
from api.services.youtube_service import get_videos_info

youtube_bp = Blueprint("youtube", __name__, url_prefix="/youtube")


@youtube_bp.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400
    try:
        scripts = fetch_and_process_transcript(video_id)
        if scripts is not None:
            return jsonify({"scripts": scripts}), 200
        else:
            return jsonify({"error": "Failed to get transcript"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@youtube_bp.route("/latest-video", methods=["GET"])
def get_latest_video():
    channel_url = request.args.get("channel_url")
    if not channel_url:
        return jsonify({"error": "Missing channel_url"}), 400
    last_video = get_latest_video_info(channel_url)
    return jsonify({"last_video": last_video}), 200


@youtube_bp.route("/videos", methods=["POST"])
def get_latest_videos():
    data = request.get_json() or {}
    channel_urls = data.get("channel_urls", [])
    stream_channel_urls = data.get("stream_channel_urls", [])

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_videos = [
            executor.submit(get_videos_info, channel_url)
            for channel_url in channel_urls
        ]

        future_streams = [
            executor.submit(get_streams_info, channel_url)
            for channel_url in stream_channel_urls
        ]

        videos = []
        for future in as_completed(future_videos + future_streams):
            try:
                result = future.result()
                if result:
                    videos.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    if videos:
        # Filter out videos with missing or None published_date
        videos_with_date = [v for v in videos if v.get("published_date")]
        sorted_videos = sorted(
            videos_with_date, key=lambda x: x["published_date"], reverse=True
        )
        filtered_videos = sorted_videos[:10]

        return jsonify(
            {
                "status": "success",
                "count": len(filtered_videos),
                "total_count": len(videos),
                "videos": filtered_videos,
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
