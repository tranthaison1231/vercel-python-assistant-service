from flask import Blueprint, request, jsonify
from api.services.transcript_service import fetch_and_process_transcript
from api.services.youtube_service import get_latest_video_info

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
