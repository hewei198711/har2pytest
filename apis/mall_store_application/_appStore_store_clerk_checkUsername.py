import os

from util.client import client

params = {
    "username": "",  # username
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_clerk_checkUsername(params=params, headers=headers):
    """
    检查用户名是否重复
    /appStore/store/clerk/checkUsername

    参数说明:
    - username: username
    """

    url = "/appStore/store/clerk/checkUsername"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
