import requests
from bs4 import BeautifulSoup


def get_123nhadatviet_news():
    """
    Scrape latest news from AWS Blog
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        # Real Python has an RSS feed that doesn't require JavaScript
        url = "https://123nhadatviet.com/rao-vat/can-ban/nha-pho/t3/da-nang.html?dientich=4&gia=18&huong=0"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse RSS/Atom feed
        soup = BeautifulSoup(response.content, "html.parser")

        list = []

        # Find all entries in the Atom feed
        entries = soup.find_all("div", class_="content-item")

        print(entries)

        for entry in entries:
            title_elem = entry.find("div", class_="ct_title")
            title = title_elem.text.strip() if title_elem else ""

            link_elem = entry.find("div", class_="ct_title").contents[0]
            link = link_elem.get("href") if link_elem else ""

            price_elem = entry.find("div", class_="ct_price")
            price = price_elem.text.strip() if price_elem else ""

            published_date_elem = entry.find("div", class_="ct_date")
            published_date = (
                published_date_elem.text.strip() if published_date_elem else ""
            )

            published_date = published_date.replace("Ngày đăng: ", "")

            area_elem = entry.find("div", class_="ct_dt")
            area = area_elem.text.strip() if area_elem else ""

            area = area.replace("Diện tích: ", "")

            horizontal_elem = entry.find("div", class_="ct_kt")
            horizontal = horizontal_elem.text.strip() if horizontal_elem else ""

            horizontal = horizontal.replace("Kích thước: ", "")

            horizontal = horizontal.split("x")[0]

            try:
                horizontal_value = float(horizontal.replace(",", "."))
            except (ValueError, AttributeError):
                horizontal_value = None

            if title and (horizontal_value is None or horizontal_value > 5):
                list.append(
                    {
                        "title": title,
                        "link": "https://123nhadatviet.com" + link,
                        "price": price,
                        "published_date": published_date,
                        "area": area,
                        "horizontal": horizontal,
                    }
                )

        return list

    except Exception as e:
        print(f"RSS feed failed, trying alternative method: {e}")
        return []
