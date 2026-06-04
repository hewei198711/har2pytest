import os

from util.client import client

data = {
    "auditOpinion": "",  # 备注
    "auditStatus": 0,  # 状态 1审核通过  2审核不通过  4已取消
    "auditType": 0,  # 操作端 1门店 2后台
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_cancelAndAudit(data=data, headers=headers):
    """
    取消/审核
    /mgmt/inventory/disManageModelChange/cancelAndAudit

    参数说明:
    - auditOpinion: 备注
    - auditStatus: 状态 1审核通过  2审核不通过  4已取消
    - auditType: 操作端 1门店 2后台
    - id: 主键id
    """

    url = "/mgmt/inventory/disManageModelChange/cancelAndAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
