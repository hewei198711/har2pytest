import os

from util.client import client

params = {
    "catalogId": 0,  # 产品分类ID
    "onlyNegative": False,  # 只看负库存
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 商品名称/商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_purchase_product_search(params=params, headers=headers):
    """
    商品搜索
    /appStore/mobile/purchase/product/search

    参数说明:
    - catalogId: 产品分类ID
    - onlyNegative: 只看负库存
    - pageNum: 页数
    - pageSize: 页大小
    - product: 商品名称/商品编码
    """

    url = "/appStore/mobile/purchase/product/search"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
