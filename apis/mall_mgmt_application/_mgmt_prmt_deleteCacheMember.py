import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_deleteCacheMember(data=data, headers=headers):
    """
    删除缓存的活动用户
    /mgmt/prmt/deleteCacheMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/deleteCacheMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
