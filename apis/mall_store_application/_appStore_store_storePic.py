import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_storePic(headers=headers):
    """
    店铺照片
    /appStore/store/storePic
    """

    url = "/appStore/store/storePic"
    with client.get(url=url, headers=headers) as r:
        return r
