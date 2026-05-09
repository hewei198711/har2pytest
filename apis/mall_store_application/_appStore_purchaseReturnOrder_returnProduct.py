import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_returnProduct(params=params, headers=headers):
    """
    获取押货退货商品信息
    /appStore/purchaseReturnOrder/returnProduct

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/purchaseReturnOrder/returnProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
