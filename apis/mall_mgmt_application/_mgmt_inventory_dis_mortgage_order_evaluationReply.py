import os

from util.client import client

data = {
    "evaluationId": 0,  # 物流评价id
    "reply": "",  # 回复
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_evaluationReply(data=data, headers=headers):
    """
    押货单物流评价回复
    /mgmt/inventory/dis/mortgage/order/evaluationReply

    参数说明:
    - evaluationId: 物流评价id
    - reply: 回复
    """

    url = "/mgmt/inventory/dis/mortgage/order/evaluationReply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
