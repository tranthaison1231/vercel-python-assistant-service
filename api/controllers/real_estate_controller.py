import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import Blueprint, jsonify

from api.services.nhadatviet_news_service import get_123nhadatviet_news
from api.services.bds68_news_service import get_bds68_news


real_estate_bp = Blueprint("real_estate", __name__, url_prefix="/real_estate")


def normalize_text(text):
    return unicodedata.normalize("NFC", text).lower()


ignore_titles = [
    "Lê Thị Riêng",
    "Xuân Thiều",
    "Trường Chinh",
    "Phước Lý",
    "sông hàn",
    "Hoà Thọ",
    "hòa hiệp",
]


@real_estate_bp.route("/news", methods=["GET"])
def get_real_estate_news():
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_123nhadatviet = executor.submit(get_123nhadatviet_news)
        future_bds68 = executor.submit(get_bds68_news)
        list = []
        for future in as_completed([future_123nhadatviet, future_bds68]):
            try:
                result = future.result()
                if result:
                    list.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    ignore_titles_normalized = [normalize_text(k) for k in ignore_titles]

    filtered_list = [
        item
        for item in list
        if not any(
            keyword in normalize_text(item["title"])
            for keyword in ignore_titles_normalized
        )
    ]

    if filtered_list:
        return jsonify(
            {
                "status": "success",
                "count": len(filtered_list),
                "list": filtered_list,
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
