import os

from util.client import client

params = {
    "likeSerialNo": "",  # likeSerialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getProductInfoList(params=params, headers=headers):
    """
    根据编码模糊搜索产品列表
    /mgmt/product/item/getProductInfoList

    参数说明:
    - likeSerialNo: likeSerialNo
    """

    url = "/mgmt/product/item/getProductInfoList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
