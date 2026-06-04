import os

from util.client import client

params = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_delete(params=params, headers=headers):
    """
    删除活动
    /mgmt/prmt/sendGift/delete

    参数说明:
    - id: 活动id
    """

    url = "/mgmt/prmt/sendGift/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
