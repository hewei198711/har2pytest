import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_cancel(params=params, headers=headers):
    """
    删除记录
    /mgmt/store/awardRecord/cancel

    参数说明:
    - id: id
    """

    url = "/mgmt/store/awardRecord/cancel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
