import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deleteAbleMemberById(data=data, headers=headers):
    """
    单个删除活动顾客
    /mgmt/prmt/luckyActivity/deleteAbleMemberById

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/deleteAbleMemberById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
