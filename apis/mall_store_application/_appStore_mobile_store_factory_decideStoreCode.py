import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_decideStoreCode(params=params, headers=headers):
    """
    根据服务中心编码判断是否为正式网点
    /appStore/mobile/store/factory/decideStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/mobile/store/factory/decideStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
