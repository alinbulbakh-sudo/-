import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ["META_ADS_ACCESS_TOKEN"]
BASE = "https://graph.facebook.com/v19.0"


def get(path, **params):
    params["access_token"] = ACCESS_TOKEN
    r = requests.get(f"{BASE}{path}", params=params)
    r.raise_for_status()
    return r.json()


def connect():
    data = get("/me", fields="name,id")
    print(f"Connected as: {data['name']} (ID: {data['id']})")
    return data


def list_ad_accounts():
    data = get("/me/adaccounts", fields="name,account_id,account_status,currency,timezone_name")
    status_map = {
        1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED",
        7: "PENDING_RISK_REVIEW", 9: "IN_GRACE_PERIOD",
        100: "PENDING_CLOSURE", 101: "CLOSED",
    }
    accounts = data.get("data", [])
    if not accounts:
        print("No ad accounts found.")
        return []
    for acc in accounts:
        status = status_map.get(acc.get("account_status"), "UNKNOWN")
        print(f"  {acc.get('name')}")
        print(f"    ID:       {acc.get('account_id')}")
        print(f"    Status:   {status}")
        print(f"    Currency: {acc.get('currency')}")
        print(f"    Timezone: {acc.get('timezone_name')}")
        print()
    return accounts


if __name__ == "__main__":
    print("=== Meta Ads Connection ===")
    connect()
    print("\n=== Ad Accounts ===")
    list_ad_accounts()
