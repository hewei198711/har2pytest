import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_queryGraduationInfoByCode(params=params, headers=headers):
    """
    根据storeCode获取最新的结业详情
    /appStore/appAndPc/store/graduation/queryGraduationInfoByCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/appAndPc/store/graduation/queryGraduationInfoByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
