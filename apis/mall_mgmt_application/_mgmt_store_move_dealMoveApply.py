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


def _mgmt_store_move_dealMoveApply(data=data, headers=headers):
    """
    受理--后台
    /mgmt/store/move/dealMoveApply

    参数说明:
    - auditOpinion: 意见
    - auditStatus: 状态 1审核通过  2已驳回
    - id: 列表数据主键id
    """

    url = "/mgmt/store/move/dealMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
