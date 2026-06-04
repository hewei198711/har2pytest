import os

from util.client import client

data = {
    "content": "",  # 审批内容
    "id": 0,  # 审批意见id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_editOpinion(data=data, headers=headers):
    """
    修改审批意见
    /mgmt/inventory/dis/mortgage/exchangeOrder/editOpinion

    参数说明:
    - content: 审批内容
    - id: 审批意见id
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/editOpinion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
