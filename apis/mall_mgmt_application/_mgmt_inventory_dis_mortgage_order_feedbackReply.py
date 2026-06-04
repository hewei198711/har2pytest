import os

from util.client import client

data = {
    "feedbackId": 0,  # 物流反馈id
    "isEstablished": 0,  # 客诉是否成立 0否 1是
    "reply": "",  # 回复
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_feedbackReply(data=data, headers=headers):
    """
    押货单物流反馈回复
    /mgmt/inventory/dis/mortgage/order/feedbackReply

    参数说明:
    - feedbackId: 物流反馈id
    - isEstablished: 客诉是否成立 0否 1是
    - reply: 回复
    """

    url = "/mgmt/inventory/dis/mortgage/order/feedbackReply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
