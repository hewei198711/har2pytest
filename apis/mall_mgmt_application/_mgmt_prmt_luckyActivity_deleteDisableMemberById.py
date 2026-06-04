import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deleteDisableMemberById(data=data, headers=headers):
    """
    单个删除不可参加顾客
    /mgmt/prmt/luckyActivity/deleteDisableMemberById

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/deleteDisableMemberById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
