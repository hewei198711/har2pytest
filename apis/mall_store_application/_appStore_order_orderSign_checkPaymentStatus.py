import os

from util.client import client

data = {
    "storeCode": "",  # 店铺编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_checkPaymentStatus(data=data, headers=headers):
    """
    店铺后台-查询签约购支付和押货订单
    /appStore/order/orderSign/checkPaymentStatus

    参数说明:
    - storeCode: 店铺编码
    """

    url = "/appStore/order/orderSign/checkPaymentStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
