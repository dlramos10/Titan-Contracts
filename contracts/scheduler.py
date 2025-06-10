
from apscheduler.schedulers.background import BackgroundScheduler
from contracts.florida_mfmp_scraper import fetch_mfmp_bids
from contracts.florida_vbs_scraper import fetch_vbs_bids
from contracts.federal_contracts import fetch_sam_gov_contracts, fetch_usa_spending
from contracts.db import save_contracts, init_db
import logging

logging.basicConfig(level=logging.INFO)

def fetch_and_save_all():
    logging.info("Fetching MFMP bids...")
    mfmp_bids = fetch_mfmp_bids()
    logging.info(f"Retrieved {len(mfmp_bids)} MFMP bids.")

    logging.info("Fetching VBS bids...")
    vbs_bids = fetch_vbs_bids()
    logging.info(f"Retrieved {len(vbs_bids)} VBS bids.")

    logging.info("Fetching SAM.gov contracts...")
    sam_bids = fetch_sam_gov_contracts(keyword="construction", naics_codes=[
        "236220", "237110", "238220", "221310", "332410"
    ])
    logging.info(f"Retrieved {len(sam_bids)} SAM.gov contracts.")

    logging.info("Fetching USAspending contracts...")
    usa_bids = fetch_usa_spending(keyword="construction", naics_codes=[
        "236220", "237110", "238220", "221310", "332410"
    ])
    logging.info(f"Retrieved {len(usa_bids)} USAspending contracts.")

    all_bids = mfmp_bids + vbs_bids + sam_bids + usa_bids
    save_contracts(all_bids)
    logging.info("Contracts saved to database.")

def start_scheduler():
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_save_all, "interval", hours=12)
    scheduler.start()
