import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_info(headers=headers):
    """
    服务中心查看基础信息
    /appStore/store/info
    """

    url = "/appStore/store/info"
    with client.get(url=url, headers=headers) as r:
        return r
