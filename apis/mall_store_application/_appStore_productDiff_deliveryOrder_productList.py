import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单号,多个单号用逗号','隔开
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_deliveryOrder_productList(params=params, headers=headers):
    """
    导入发货单获取对应商品的列表
    /appStore/productDiff/deliveryOrder/productList

    参数说明:
    - deliverSnList: 发货单号,多个单号用逗号','隔开
    """

    url = "/appStore/productDiff/deliveryOrder/productList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
