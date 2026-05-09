import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_graduationCheckByStoreCode(params=params, headers=headers):
    """
    结业转店处理验证服务中心
    /appStore/appAndPc/store/graduation/graduationCheckByStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/appAndPc/store/graduation/graduationCheckByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
