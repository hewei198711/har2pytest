import os

from util.client import client

params = {
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_reviewConfigList(params=params, headers=headers):
    """
    年审模块配置列表(type 1,2,3,4 全部则null)
    /appStore/store/reviewConfigList

    参数说明:
    - type: type
    """

    url = "/appStore/store/reviewConfigList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
