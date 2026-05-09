import os

from util.client import client

params = {
    "orderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_getProductsForEdit(params=params, headers=headers):
    """
    编辑押货单查询最新的商品列表
    /appStore/store/dis/mortgageOrder/getProductsForEdit

    参数说明:
    - orderId: 押货单id
    """

    url = "/appStore/store/dis/mortgageOrder/getProductsForEdit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
