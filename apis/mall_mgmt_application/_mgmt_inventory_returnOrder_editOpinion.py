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


def _mgmt_inventory_returnOrder_editOpinion(data=data, headers=headers):
    """
    后台押货退货修改审批意见
    /mgmt/inventory/returnOrder/editOpinion

    参数说明:
    - content: 审批内容
    - id: 审批意见id
    """

    url = "/mgmt/inventory/returnOrder/editOpinion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
