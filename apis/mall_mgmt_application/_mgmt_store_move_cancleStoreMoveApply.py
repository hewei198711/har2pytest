import os

from util.client import client

data = {
    "cancelApplication": [],  # 撤销申请书
    "cancelReason": "",  # 撤销原因
    "id": 0,  # 主键id
    "port": 0,  # 请求端 0后台 1APP 2PC
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_move_cancleStoreMoveApply(data=data, headers=headers):
    """
    取消搬迁申请----web,app,后台
    /mgmt/store/move/cancleStoreMoveApply

    参数说明:
    - cancelApplication: 撤销申请书
    - cancelReason: 撤销原因
    - id: 主键id
    - port: 请求端 0后台 1APP 2PC
    """

    url = "/mgmt/store/move/cancleStoreMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
