import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_deliverInfo_orderNo(params=params, headers=headers):
    """
    订单物流轨迹
    /mgmt/order/deliverInfo/{orderNo}

    参数说明:
    - orderNo: orderNo
    """

    url = f"/mgmt/order/deliverInfo/{params['orderNo']}"
    with client.get(url=url, headers=headers) as r:
        return r
