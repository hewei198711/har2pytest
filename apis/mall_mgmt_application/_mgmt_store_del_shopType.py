import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_del_shopType(params=params, headers=headers):
    """
    删除网点类型
    /mgmt/store/del/shopType

    参数说明:
    - id: id
    """

    url = "/mgmt/store/del/shopType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
