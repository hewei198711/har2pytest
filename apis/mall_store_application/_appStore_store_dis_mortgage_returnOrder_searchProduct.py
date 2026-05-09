import os

from util.client import client

params = {
    "productCode": "",  # 商品关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_searchProduct(params=params, headers=headers):
    """
    商品编码搜索退货商品信息
    /appStore/store/dis/mortgage/returnOrder/searchProduct

    参数说明:
    - productCode: 商品关键字
    """

    url = "/appStore/store/dis/mortgage/returnOrder/searchProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
