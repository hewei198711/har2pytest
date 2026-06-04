import os

from util.client import client

params = {
    "mortgageNum": 0,  # mortgageNum
    "productCode": "",  # productCode
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_updateMortgageNumByDif(params=params, headers=headers):
    """
    修改已押货数
    /mgmt/inventory/distribution/updateMortgageNumByDif

    参数说明:
    - mortgageNum: mortgageNum
    - productCode: productCode
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/distribution/updateMortgageNumByDif"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
