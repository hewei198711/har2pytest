import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "store",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_isStoreInTrafficControl(headers=headers):
    """
    TODO: 添加接口描述
    /appStore/common/isStoreInTrafficControl
    """

    url = "/appStore/common/isStoreInTrafficControl"
    with client.get(url=url, headers=headers) as r:
        return r
