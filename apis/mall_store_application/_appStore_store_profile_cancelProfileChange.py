import os

from util.client import client

data = {
    "id": 0,  # 变更ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_cancelProfileChange(data=data, headers=headers):
    """
    取消服务中心资料变更
    /appStore/store/profile/cancelProfileChange

    参数说明:
    - id: 变更ID
    """

    url = "/appStore/store/profile/cancelProfileChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
