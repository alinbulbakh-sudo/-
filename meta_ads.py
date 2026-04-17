import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User

load_dotenv()

ACCESS_TOKEN = os.environ["META_ADS_ACCESS_TOKEN"]


def connect():
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)
    me = User(fbid="me")
    info = me.api_get(fields=["name", "id"])
    print(f"Connected as: {info['name']} (ID: {info['id']})")
    return info


def list_ad_accounts():
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)
    me = User(fbid="me")
    accounts = me.get_ad_accounts(fields=[
        AdAccount.Field.name,
        AdAccount.Field.account_id,
        AdAccount.Field.account_status,
        AdAccount.Field.currency,
        AdAccount.Field.timezone_name,
    ])
    for account in accounts:
        status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW", 9: "IN_GRACE_PERIOD", 100: "PENDING_CLOSURE", 101: "CLOSED", 201: "ANY_ACTIVE", 202: "ANY_CLOSED"}
        status = status_map.get(account.get(AdAccount.Field.account_status), "UNKNOWN")
        print(f"  Account: {account[AdAccount.Field.name]}")
        print(f"    ID:       {account[AdAccount.Field.account_id]}")
        print(f"    Status:   {status}")
        print(f"    Currency: {account.get(AdAccount.Field.currency)}")
        print(f"    Timezone: {account.get(AdAccount.Field.timezone_name)}")
        print()
    return accounts


if __name__ == "__main__":
    print("=== Meta Ads Connection ===")
    connect()
    print("\n=== Ad Accounts ===")
    list_ad_accounts()
