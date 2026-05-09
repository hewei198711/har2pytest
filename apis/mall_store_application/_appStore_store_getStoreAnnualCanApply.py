import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getStoreAnnualCanApply(params=params, headers=headers):
    """
    获取店铺可发起年审项目列表
    /appStore/store/getStoreAnnualCanApply

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/getStoreAnnualCanApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
