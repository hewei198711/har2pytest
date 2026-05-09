import os

from util.client import client

params = {
    "reviewModelType": "",  # 年审类型
    "reviewTitle": "",  # 年审标题
    "storeCode": "",  # 店号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_isExit(params=params, headers=headers):
    """
    年审项目是否已存在
    /appStore/store/isExit

    参数说明:
    - reviewModelType: 年审类型
    - reviewTitle: 年审标题
    - storeCode: 店号
    """

    url = "/appStore/store/isExit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
