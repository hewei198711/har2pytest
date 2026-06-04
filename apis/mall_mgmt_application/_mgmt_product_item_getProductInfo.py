import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getProductInfo(params=params, headers=headers):
    """
    根据产品编码查询产品
    /mgmt/product/item/getProductInfo

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/product/item/getProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
