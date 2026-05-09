import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_lastRecord(params=params, headers=headers):
    """
    查询服务中心最新生效的获奖记录
    /appStore/store/lastRecord

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/lastRecord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
