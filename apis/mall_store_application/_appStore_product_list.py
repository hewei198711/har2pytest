import os

from util.client import client

params = {
    "catalogId": "",  # 商品分类Id
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productTitle": "",  # 商品名称
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_product_list(params=params, headers=headers):
    """
    产品列表
    /appStore/product/list

    参数说明:
    - catalogId: 商品分类Id
    - pageNum: 页数
    - pageSize: 页大小
    - productTitle: 商品名称
    - serialNo: 商品编码
    """

    url = "/appStore/product/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
