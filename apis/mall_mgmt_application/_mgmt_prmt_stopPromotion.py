import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_stopPromotion(data=data, headers=headers):
    """
    手动停止活动
    /mgmt/prmt/stopPromotion

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/stopPromotion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
