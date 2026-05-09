import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getStoreAddressInfo(headers=headers):
    """
    服务中心地址信息
    /appStore/store/getStoreAddressInfo
    """

    url = "/appStore/store/getStoreAddressInfo"
    with client.get(url=url, headers=headers) as r:
        return r
