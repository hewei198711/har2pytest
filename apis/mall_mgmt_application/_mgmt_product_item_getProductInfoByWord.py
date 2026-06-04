import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getProductInfoByWord(params=params, headers=headers):
    """
    根据产品编码或名称关键字查询产品
    /mgmt/product/item/getProductInfoByWord

    参数说明:
    - keyword: keyword
    """

    url = "/mgmt/product/item/getProductInfoByWord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
