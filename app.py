
from flask import Flask, render_template, request, redirect, url_for
from contracts.scheduler import start_scheduler
from contracts.db import fetch_all_contracts, save_contracts, init_db
from contracts.federal_contracts import fetch_sam_gov_contracts, fetch_usa_spending
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET"])
def search():
    contracts = fetch_all_contracts()
    return render_template("results.html", contracts=contracts)

@app.route("/contract/<string:contract_id>")
def contract_detail(contract_id):
    all_contracts = fetch_all_contracts()
    contract = next((c for c in all_contracts if c["id"] == contract_id), None)
    return render_template("contract_detail.html", contract=contract)

@app.route("/dashboard")
def dashboard():
    contracts = fetch_all_contracts()
    sources = {}
    for c in contracts:
        src = c["source"]
        sources[src] = sources.get(src, 0) + 1
    return render_template("dashboard.html", contracts=contracts, sources=sources)

@app.route("/fetch_federal", methods=["POST"])
def fetch_federal():
    sam = fetch_sam_gov_contracts(keyword="construction", naics_codes=[
        "236220", "237110", "238220", "221310", "332410"
    ])
    usa = fetch_usa_spending(keyword="construction", naics_codes=[
        "236220", "237110", "238220", "221310", "332410"
    ])
    save_contracts(sam + usa)
    return redirect(url_for("search"))

if __name__ == "__main__":
    os.makedirs("db", exist_ok=True)
    init_db()
    start_scheduler()
    app.run(debug=True)
