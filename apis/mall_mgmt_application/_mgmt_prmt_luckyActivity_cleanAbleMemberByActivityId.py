import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_cleanAbleMemberByActivityId(data=data, headers=headers):
    """
    清空活动顾客
    /mgmt/prmt/luckyActivity/cleanAbleMemberByActivityId

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/cleanAbleMemberByActivityId"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
