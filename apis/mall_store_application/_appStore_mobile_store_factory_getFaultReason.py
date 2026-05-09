import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_getFaultReason(headers=headers):
    """
    获取故障原因
    /appStore/mobile/store/factory/getFaultReason
    """

    url = "/appStore/mobile/store/factory/getFaultReason"
    with client.get(url=url, headers=headers) as r:
        return r
