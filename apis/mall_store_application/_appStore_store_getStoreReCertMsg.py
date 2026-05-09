import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getStoreReCertMsg(headers=headers):
    """
    获取店铺端重新认证消息
    /appStore/store/getStoreReCertMsg
    """

    url = "/appStore/store/getStoreReCertMsg"
    with client.get(url=url, headers=headers) as r:
        return r
