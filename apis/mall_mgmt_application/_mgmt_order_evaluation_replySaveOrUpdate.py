import os

from util.client import client

data = {
    "evaluateId": 0,  # 订单评价ID
    "replyContent": "",  # 订单评价回复内容
    "replyId": 0,  # 订单评价回复ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_replySaveOrUpdate(data=data, headers=headers):
    """
    replySaveOrUpdate
    /mgmt/order/evaluation/replySaveOrUpdate

    参数说明:
    - evaluateId: 订单评价ID
    - replyContent: 订单评价回复内容
    - replyId: 订单评价回复ID
    """

    url = "/mgmt/order/evaluation/replySaveOrUpdate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
