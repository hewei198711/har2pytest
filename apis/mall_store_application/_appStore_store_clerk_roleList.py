import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_clerk_roleList(headers=headers):
    """
    获取店员账号角色
    /appStore/store/clerk/roleList
    """

    url = "/appStore/store/clerk/roleList"
    with client.get(url=url, headers=headers) as r:
        return r
