import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_isStoreInTrafficControl(headers=headers):
    """
    店铺是否处于交通管控
    /appStore/common/isStoreInTrafficControl
    """

    url = "/appStore/common/isStoreInTrafficControl"
    with client.get(url=url, headers=headers) as r:
        return r
