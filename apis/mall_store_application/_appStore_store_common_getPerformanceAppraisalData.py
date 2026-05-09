import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
    "year": 0,  # year
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_common_getPerformanceAppraisalData(params=params, headers=headers):
    """
    获取服务中心业绩看板考核数据
    /appStore/store/common/getPerformanceAppraisalData

    参数说明:
    - storeCode: storeCode
    - year: year
    """

    url = "/appStore/store/common/getPerformanceAppraisalData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
