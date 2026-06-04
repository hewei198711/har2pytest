import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_deleteShareTask(data=data, headers=headers):
    """
    删除分享领券活动
    /mgmt/prmt/share/deleteShareTask

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/share/deleteShareTask"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
