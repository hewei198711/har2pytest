import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getProductInfo(params=params, headers=headers):
    """
    获取商品信息
    /mgmt/inventory/common/getProductInfo

    参数说明:
    - productCode: productCode
    """

    url = "/mgmt/inventory/common/getProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
