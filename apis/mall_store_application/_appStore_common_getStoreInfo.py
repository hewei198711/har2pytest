import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getStoreInfo(params=params, headers=headers):
    """
    获取服务中心信息
    /appStore/common/getStoreInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/common/getStoreInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
