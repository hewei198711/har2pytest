import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_getMortgageAmountInfo(params=params, headers=headers):
    """
    获取押货额详情
    /mgmt/inventory/mortgageAmount/getMortgageAmountInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/getMortgageAmountInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
