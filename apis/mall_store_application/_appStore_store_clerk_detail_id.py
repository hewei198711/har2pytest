import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_clerk_detail_id(params=params, headers=headers):
    """
    获取店员账号信息
    /appStore/store/clerk/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/store/clerk/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
