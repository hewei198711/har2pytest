import os

from util.client import client

data = {
    "exId": 0,  # 关联外键
    "idList": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_batchDeleteDisableMember(data=data, headers=headers):
    """
    批量删除不可参加顾客
    /mgmt/prmt/luckyActivity/batchDeleteDisableMember

    参数说明:
    - exId: 关联外键
    """

    url = "/mgmt/prmt/luckyActivity/batchDeleteDisableMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
