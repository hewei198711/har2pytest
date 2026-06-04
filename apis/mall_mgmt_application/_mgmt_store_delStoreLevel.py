import os

from util.client import client

data = {
    "id": 0,  # 主键ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_delStoreLevel(data=data, headers=headers):
    """
    删除网点等级
    /mgmt/store/delStoreLevel

    参数说明:
    - id: 主键ID
    """

    url = "/mgmt/store/delStoreLevel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
