import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_deposit_msg(headers=headers):
    """
    获取服务中心可用押货保证金余额
    /appStore/store/deposit/msg
    """

    url = "/appStore/store/deposit/msg"
    with client.get(url=url, headers=headers) as r:
        return r
