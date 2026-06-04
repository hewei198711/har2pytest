import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getProductByCode(params=params, headers=headers):
    """
    根据一或二级编码精确商品信息
    /mgmt/inventory/common/getProductByCode

    参数说明:
    - productCode: productCode
    """

    url = "/mgmt/inventory/common/getProductByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
