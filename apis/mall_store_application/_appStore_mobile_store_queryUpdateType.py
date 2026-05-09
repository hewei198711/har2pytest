import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_queryUpdateType(params=params, headers=headers):
    """
    app服务中心-查询可修改类型
    /appStore/mobile/store/queryUpdateType

    参数说明:
    - cardNo: cardNo
    """

    url = "/appStore/mobile/store/queryUpdateType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
