import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_getMortgageAmountByStore(params=params, headers=headers):
    """
    根据storeCode查询押货余额主表数据
    /mgmt/inventory/mortgageAmount/getMortgageAmountByStore

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/getMortgageAmountByStore"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
