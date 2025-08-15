from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Blueprint, jsonify

from api.services.get_github_trending_service import get_github_trending_service

github_bp = Blueprint("github", __name__, url_prefix="/github")


@github_bp.route("/news", methods=["GET"])
def get_trending_repositories():
    with ThreadPoolExecutor(max_workers=2) as executor:
        python_repos = executor.submit(get_github_trending_service, "python")
        typescript_repos = executor.submit(get_github_trending_service, "typescript")

        repositories = []
        for future in as_completed([python_repos, typescript_repos]):
            try:
                result = future.result()
                if result:
                    repositories.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    sorted_repositories = sorted(repositories, key=lambda x: x["stars"], reverse=True)

    if sorted_repositories:
        return jsonify(
            {
                "status": "success",
                "count": len(sorted_repositories),
                "repositories": sorted_repositories,
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
