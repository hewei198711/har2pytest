import os

from util.client import client

params = {
    "type": 0,  # 提示语内容类型：1-首页，2-押货保证金管理
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getManageWordContent(params=params, headers=headers):
    """
    获取服务中心提示语内容
    /appStore/store/getManageWordContent

    参数说明:
    - type: 提示语内容类型：1-首页，2-押货保证金管理
    """

    url = "/appStore/store/getManageWordContent"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
