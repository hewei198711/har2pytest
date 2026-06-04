import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deleteActivity(data=data, headers=headers):
    """
    抽奖活动-删除
    /mgmt/prmt/luckyActivity/deleteActivity

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/deleteActivity"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
