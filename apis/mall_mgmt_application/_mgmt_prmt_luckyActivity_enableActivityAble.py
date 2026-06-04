import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_enableActivityAble(data=data, headers=headers):
    """
    启用活动顾客
    /mgmt/prmt/luckyActivity/enableActivityAble

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/enableActivityAble"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
