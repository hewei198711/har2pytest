import os

from util.client import client

data = {
    "productShelvesKeyword": "",  # 货架关联关联词
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_productShelves_getShelvesProductList(data=data, headers=headers):
    """
    获取货架商品列表
    /appStore/msym/productShelves/getShelvesProductList

    参数说明:
    - productShelvesKeyword: 货架关联关联词
    """

    url = "/appStore/msym/productShelves/getShelvesProductList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
