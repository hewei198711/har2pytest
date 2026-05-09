import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_getMainStoreInfo(params=params, headers=headers):
    """
    根据服务中心编号获取服务信息--仅仅主表信息
    /appStore/appAndPc/store/graduation/getMainStoreInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/appAndPc/store/graduation/getMainStoreInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
