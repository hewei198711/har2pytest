import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_getAvailableAmount(params=params, headers=headers):
    """
    根据storeCode查询押货余额
    /mgmt/inventory/mortgageAmount/getAvailableAmount

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/getAvailableAmount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
