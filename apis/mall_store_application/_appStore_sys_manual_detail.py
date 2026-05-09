import os

from util.client import client

params = {
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_manual_detail(params=params, headers=headers):
    """
    获取形象手册详情
    /appStore/sys/manual/detail

    参数说明:
    - type: type
    """

    url = "/appStore/sys/manual/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
