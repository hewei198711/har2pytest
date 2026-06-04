import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_searchProductListByKeyword(params=params, headers=headers):
    """
    关键字查询组合商品列表
    /mgmt/product/item/searchProductListByKeyword

    参数说明:
    - keyword: keyword
    """

    url = "/mgmt/product/item/searchProductListByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
