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


def _mgmt_inventory_mortgageAmount_exportCheckMortgageAndStock(params=params, headers=headers):
    """
    押货余额与库存差异对比导出
    /mgmt/inventory/mortgageAmount/exportCheckMortgageAndStock

    参数说明:
    - companyCode: companyCode
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/exportCheckMortgageAndStock"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
