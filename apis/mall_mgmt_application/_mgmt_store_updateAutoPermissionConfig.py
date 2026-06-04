import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_updateAutoPermissionConfig(headers=headers):
    """
    更新经营模式权限配置内容
    /mgmt/store/updateAutoPermissionConfig
    """

    url = "/mgmt/store/updateAutoPermissionConfig"
    with client.post(url=url, headers=headers) as r:
        return r
