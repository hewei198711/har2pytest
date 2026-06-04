import os

from util.client import client

data = {
    "auditOpinion": "",  # 意见
    "auditStatus": 0,  # 状态 1审核通过  2已驳回
    "id": 0,  # 列表数据主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_move_updateStoreMoveApply(data=data, headers=headers):
    """
    审批搬迁申请记录--后台
    /mgmt/store/move/updateStoreMoveApply

    参数说明:
    - auditOpinion: 意见
    - auditStatus: 状态 1审核通过  2已驳回
    - id: 列表数据主键id
    """

    url = "/mgmt/store/move/updateStoreMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
