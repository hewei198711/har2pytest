import os

from util.client import client

data = {
    "orderNo": "",  # 订单编号
    "returnNo": "",  # 退货单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_refund(data=data, headers=headers):
    """
    发起退款
    /mgmt/order/return/refund

    参数说明:
    - orderNo: 订单编号
    - returnNo: 退货单号
    """

    url = "/mgmt/order/return/refund"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
