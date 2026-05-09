import os

from util.client import client

params = {
    "orderNo": "",  # 订单编号(必填)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_delivery(params=params, headers=headers):
    """
    根据单号查询物流信息
    /appStore/order/delivery

    参数说明:
    - orderNo: 订单编号(必填)
    """

    url = "/appStore/order/delivery"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
