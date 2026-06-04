import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_graduation_queryGraduationInfoByCode(params=params, headers=headers):
    """
    根据storeCode获取最新的结业详情
    /mgmt/store/graduation/queryGraduationInfoByCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/graduation/queryGraduationInfoByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
