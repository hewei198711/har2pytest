import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_PurchaseOrderApply_getProductsByOrderSn(params=params, headers=headers):
    """
    根据押货单号获取对应商品信息
    /appStore/PurchaseOrderApply/getProductsByOrderSn

    参数说明:
    - orderSn: orderSn
    """

    url = "/appStore/PurchaseOrderApply/getProductsByOrderSn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
