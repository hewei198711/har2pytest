import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_print(params=params, headers=headers):
    """
    打印发货单
    /appStore/order/print

    参数说明:
    - orderNo: orderNo
    """

    url = "/appStore/order/print"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
