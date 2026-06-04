import os

from util.client import client

data = {
    "content": "",  # 审批内容
    "orderId": 0,  # 押货或售后单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_opinion(data=data, headers=headers):
    """
    添加审批意见
    /mgmt/inventory/dis/mortgage/returnOrder/opinion

    参数说明:
    - content: 审批内容
    - orderId: 押货或售后单id
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/opinion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
