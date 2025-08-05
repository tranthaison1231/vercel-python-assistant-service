import requests
from bs4 import BeautifulSoup


def get_bds68_news():
    """
    Scrape latest news from AWS Blog
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        # Real Python has an RSS feed that doesn't require JavaScript
        url = "https://bds68.com.vn/ban-dat-nen/da-nang?gia=3000-4500&dientich=80-100"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse RSS/Atom feed
        soup = BeautifulSoup(response.content, "html.parser")

        list = []

        # Find all entries in the Atom feed
        entries = soup.find_all("div", class_="prop-box-item-contain")

        for entry in entries:
            title_elem = entry.find("div", class_="header-prop-title").find("a")
            title = title_elem.text.strip() if title_elem else ""

            link_elem = entry.find("div", class_="header-prop-title").find("a")
            link = link_elem.get("href") if link_elem else ""

            price_elem = entry.find("div", class_="prop-price-lotsize")

            price = ""
            if price_elem:
                price_span = price_elem.find("span", class_="prop-item-info")
                if price_span:
                    price = price_span.text.strip()

            published_date = ""
            published_date_elem = entry.find("div", class_="prop-grid-date")
            if published_date_elem:
                span = published_date_elem.find("span")
                if span:
                    published_date = span.text.strip()

            area_elem = entry.find("div", class_="prop-price-lotsize")

            area = ""
            if area_elem:
                area_spans = area_elem.find_all("span", class_="prop-item-info")
                if len(area_spans) > 1:
                    area = area_spans[1].text.strip()

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
                        "link": "https://bds68.com.vn" + link,
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
