import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_getAllManuals(headers=headers):
    """
    获取所有手册、案例库配置
    /appStore/sys/getAllManuals
    """

    url = "/appStore/sys/getAllManuals"
    with client.get(url=url, headers=headers) as r:
        return r
