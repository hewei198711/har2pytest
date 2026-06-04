import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_close(data=data, headers=headers):
    """
    关闭活动
    /mgmt/prmt/passwordActivity/close

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/passwordActivity/close"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
