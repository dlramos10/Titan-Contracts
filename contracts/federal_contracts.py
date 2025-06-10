
import requests
from datetime import datetime, timedelta
import os

SAM_API_KEY = os.getenv("SAM_API_KEY") or "your_api_key_here"

def fetch_sam_gov_contracts(keyword="construction", naics_codes=[], start_date=None, end_date=None):
    base_url = "https://api.sam.gov/prod/opportunities/v2/search"
    headers = {"Accept": "application/json"}

    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%m/%d/%Y")
    if not end_date:
        end_date = datetime.utcnow().strftime("%m/%d/%Y")

    params = {
        "api_key": SAM_API_KEY,
        "q": keyword,
        "postedFrom": start_date,
        "postedTo": end_date,
        "noticeType": "Combined Synopsis/Solicitation",
        "limit": 10,
    }
    if naics_codes:
        params["naics"] = ",".join(naics_codes)

    r = requests.get(base_url, headers=headers, params=params)
    results = []
    if r.status_code == 200:
        data = r.json()
        for item in data.get("opportunitiesData", []):
            results.append({
                "id": item.get("noticeId"),
                "title": item.get("title"),
                "url": item.get("uiLink"),
                "source": "SAM.gov",
                "agency": item.get("agency", {}).get("name", ""),
                "publishDate": item.get("postedDate", ""),
                "deadline": item.get("responseDeadLine", ""),
                "naics": item.get("naics", "")
            })
    return results

def fetch_usa_spending(keyword="construction", naics_codes=[]):
    base_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    body = {
        "filters": {
            "award_type_codes": ["A", "B", "C", "D"],
            "keywords": [keyword]
        },
        "fields": ["Award ID", "Recipient Name", "Start Date", "Award Amount", "NAICS Code", "Awarding Agency Name"],
        "limit": 10,
        "page": 1,
        "sort": "Award Amount",
        "order": "desc"
    }
    if naics_codes:
        body["filters"]["naics_codes"] = naics_codes

    r = requests.post(base_url, json=body)
    results = []
    if r.status_code == 200:
        data = r.json()
        for row in data.get("results", []):
            results.append({
                "id": row.get("Award ID"),
                "title": row.get("Recipient Name"),
                "url": "",  # no direct URL
                "source": "USAspending",
                "agency": row.get("Awarding Agency Name", ""),
                "publishDate": row.get("Start Date", ""),
                "deadline": "",
                "naics": row.get("NAICS Code", "")
            })
    return results
