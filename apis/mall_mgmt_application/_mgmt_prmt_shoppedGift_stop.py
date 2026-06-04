import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_stop(data=data, headers=headers):
    """
    停止
    /mgmt/prmt/shoppedGift/stop

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/shoppedGift/stop"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
