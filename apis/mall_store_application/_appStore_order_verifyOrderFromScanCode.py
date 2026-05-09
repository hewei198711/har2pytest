import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_verifyOrderFromScanCode(params=params, headers=headers):
    """
    店铺校验客户订单二维码
    /appStore/order/verifyOrderFromScanCode

    参数说明:
    - orderNo: orderNo
    """

    url = "/appStore/order/verifyOrderFromScanCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
