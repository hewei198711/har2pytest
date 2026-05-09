import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getCurrentUser(headers=headers):
    """
    获取当前登录用户信息
    /appStore/common/getCurrentUser
    """

    url = "/appStore/common/getCurrentUser"
    with client.get(url=url, headers=headers) as r:
        return r
