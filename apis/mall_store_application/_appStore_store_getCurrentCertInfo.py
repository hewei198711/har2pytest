import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getCurrentCertInfo(headers=headers):
    """
    获取当前电子印章信息
    /appStore/store/getCurrentCertInfo
    """

    url = "/appStore/store/getCurrentCertInfo"
    with client.get(url=url, headers=headers) as r:
        return r
