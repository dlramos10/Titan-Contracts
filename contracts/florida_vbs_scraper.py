
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_vbs_bids():
    url = "https://www.myflorida.com/apps/vbs/vbs_www.main_menu"  # Static menu page
    session = requests.Session()
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    table = soup.find("table")
    if not table:
        return results

    rows = table.find_all("tr")[1:]  # Skip header
    for row in rows[:20]:  # Limit to top 20 entries
        cols = row.find_all("td")
        if len(cols) >= 2:
            title = cols[1].get_text(strip=True)
            link = "https://www.myflorida.com" + cols[1].find("a")["href"] if cols[1].find("a") else ""
            results.append({
                "id": link,
                "title": title,
                "url": link,
                "source": "Florida VBS",
                "agency": "Various Florida Agencies",
                "publishDate": "",
                "deadline": "",
                "naics": ""
            })

    return results
