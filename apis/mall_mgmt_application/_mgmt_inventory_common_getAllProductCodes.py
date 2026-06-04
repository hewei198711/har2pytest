import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getAllProductCodes(params=params, headers=headers):
    """
    获取所有的商品编码列表
    /mgmt/inventory/common/getAllProductCodes

    参数说明:
    - productCode: productCode
    """

    url = "/mgmt/inventory/common/getAllProductCodes"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
