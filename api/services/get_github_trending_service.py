import requests
from bs4 import BeautifulSoup
import re


def get_github_trending_service(language: str):
    try:
        # Scrape GitHub's trending page
        url = f"https://github.com/trending/{language}?since=daily"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all repository articles
        repo_articles = soup.find_all("article", class_="Box-row")

        repositories = []
        for article in repo_articles[:10]:  # Limit to top 10
            try:
                # Extract repository name and owner
                repo_link = article.find("h2", class_="h3 lh-condensed").find("a")
                if not repo_link:
                    continue

                full_name = repo_link.get_text(strip=True)
                repo_url = "https://github.com" + repo_link.get("href")

                # Extract description
                description_elem = article.find("p")
                description = (
                    description_elem.get_text(strip=True) if description_elem else ""
                )

                # Extract stars
                stars_elem = article.find("a", href=re.compile(r"/stargazers"))
                stars = 0
                if stars_elem:
                    stars_text = stars_elem.get_text(strip=True)
                    # Handle "1.2k" format
                    if "k" in stars_text:
                        stars = int(float(stars_text.replace("k", "")) * 1000)
                    else:
                        stars = int(stars_text.replace(",", ""))

                # Extract forks
                forks_elem = article.find("a", href=re.compile(r"/forks"))
                forks = 0
                if forks_elem:
                    forks_text = forks_elem.get_text(strip=True)
                    if "k" in forks_text:
                        forks = int(float(forks_text.replace("k", "")) * 1000)
                    else:
                        forks = int(forks_text.replace(",", ""))

                # Extract stars gained today
                stars_today_elem = article.find(
                    "span", class_="d-inline-block float-sm-right"
                )
                stars_today = 0
                if stars_today_elem:
                    stars_text = stars_today_elem.get_text(strip=True)
                    # Extract number from "423 stars today"
                    match = re.search(r"(\d+(?:\.\d+)?[km]?)", stars_text)
                    if match:
                        stars_today_text = match.group(1)
                        if "k" in stars_today_text:
                            stars_today = int(
                                float(stars_today_text.replace("k", "")) * 1000
                            )
                        elif "m" in stars_today_text:
                            stars_today = int(
                                float(stars_today_text.replace("m", "")) * 1000000
                            )
                        else:
                            stars_today = int(stars_today_text)

                repositories.append(
                    {
                        "name": full_name.split("/")[-1]
                        if "/" in full_name
                        else full_name,
                        "full_name": full_name,
                        "description": description,
                        "language": language,
                        "stars": stars,
                        "forks": forks,
                        "stars_today": stars_today,
                        "url": repo_url,
                        "owner": full_name.split("/")[0] if "/" in full_name else "",
                    }
                )

            except Exception as e:
                print(f"Error parsing repository: {e}")
                continue

        return repositories

    except requests.exceptions.RequestException:
        return None
