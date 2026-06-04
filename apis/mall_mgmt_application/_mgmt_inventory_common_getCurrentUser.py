import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getCurrentUser(headers=headers):
    """
    获取当前登录用户信息
    /mgmt/inventory/common/getCurrentUser
    """

    url = "/mgmt/inventory/common/getCurrentUser"
    with client.get(url=url, headers=headers) as r:
        return r
