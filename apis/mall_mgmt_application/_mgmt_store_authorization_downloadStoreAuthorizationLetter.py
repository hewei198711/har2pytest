import os

from util.client import client

params = {
    "downloadType": 0,  # 下载途径，1：运营后台，2：门店系统
    "id": 0,  # 主键ID
    "type": 0,  # 类型，1：预览，2：下载
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_downloadStoreAuthorizationLetter(params=params, headers=headers):
    """
    下载授权书
    /mgmt/store/authorization/downloadStoreAuthorizationLetter

    参数说明:
    - downloadType: 下载途径，1：运营后台，2：门店系统
    - id: 主键ID
    - type: 类型，1：预览，2：下载
    """

    url = "/mgmt/store/authorization/downloadStoreAuthorizationLetter"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
