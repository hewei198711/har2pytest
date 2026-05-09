import os

from util.client import client

data = {
    "productList": [],  # 商品编号列表
    "productShelvesKeyword": "",  # 货架关联关联词
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_productShelves_saveShelvesProducts(data=data, headers=headers):
    """
    保存货架对应的商品
    /appStore/msym/productShelves/saveShelvesProducts

    参数说明:
    - productList: 商品编号列表
    - productShelvesKeyword: 货架关联关联词
    """

    url = "/appStore/msym/productShelves/saveShelvesProducts"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
