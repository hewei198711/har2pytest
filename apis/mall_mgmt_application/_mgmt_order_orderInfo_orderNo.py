import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderInfo_orderNo(params=params, headers=headers):
    """
    订单信息
    /mgmt/order/orderInfo/{orderNo}

    参数说明:
    - orderNo: orderNo
    """

    url = f"/mgmt/order/orderInfo/{params['orderNo']}"
    with client.get(url=url, headers=headers) as r:
        return r
