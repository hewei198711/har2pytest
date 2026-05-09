import os

from util.client import client

params = {
    "keyword": "",  # 商品关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_searchProductsByKeyword(params=params, headers=headers):
    """
    关键字获取服务中心库存商品
    /appStore/store/dis/mortgage/returnOrder/searchProductsByKeyword

    参数说明:
    - keyword: 商品关键字
    """

    url = "/appStore/store/dis/mortgage/returnOrder/searchProductsByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
