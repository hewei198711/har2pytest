import os

from util.client import client

params = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_delete(params=params, headers=headers):
    """
    删除活动
    /mgmt/prmt/puzzle/delete

    参数说明:
    - id: 活动id
    """

    url = "/mgmt/prmt/puzzle/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
