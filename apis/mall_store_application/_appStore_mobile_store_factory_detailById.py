import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_detailById(params=params, headers=headers):
    """
    根据ID获取返修单
    /appStore/mobile/store/factory/detailById

    参数说明:
    - id: id
    """

    url = "/appStore/mobile/store/factory/detailById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
