import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getStoreManagerCertInfo(headers=headers):
    """
    获取管理员个人认证信息
    /appStore/store/getStoreManagerCertInfo
    """

    url = "/appStore/store/getStoreManagerCertInfo"
    with client.get(url=url, headers=headers) as r:
        return r
