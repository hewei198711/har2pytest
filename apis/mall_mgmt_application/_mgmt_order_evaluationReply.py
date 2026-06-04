import os

from util.client import client

data = {
    "orderId": 0,  # 订单ID
    "reply": "",  # 回复内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluationReply(data=data, headers=headers):
    """
    回复物流评价
    /mgmt/order/evaluationReply

    参数说明:
    - orderId: 订单ID
    - reply: 回复内容
    """

    url = "/mgmt/order/evaluationReply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
