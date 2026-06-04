import os

from util.client import client

params = {
    "companyCode": "",  # companyCode
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_checkMortgageAndStock(params=params, headers=headers):
    """
    押货余额与库存差异对比
    /mgmt/inventory/mortgageAmount/checkMortgageAndStock

    参数说明:
    - companyCode: companyCode
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/checkMortgageAndStock"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
