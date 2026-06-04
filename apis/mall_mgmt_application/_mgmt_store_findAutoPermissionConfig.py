import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_findAutoPermissionConfig(headers=headers):
    """
    查询经营模式权限配置内容
    /mgmt/store/findAutoPermissionConfig
    """

    url = "/mgmt/store/findAutoPermissionConfig"
    with client.get(url=url, headers=headers) as r:
        return r
