import os

from util.client import client

params = {
    "month": 0,  # month
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_deposit_realTimeBill(params=params, headers=headers):
    """
    实时账款对账单查询
    /mgmt/inventory/deposit/realTimeBill

    参数说明:
    - month: month
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/deposit/realTimeBill"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
