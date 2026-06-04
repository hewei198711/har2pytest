import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_weshop_importPermission(headers=headers):
    """
    导入KOS转分权限
    /mgmt/weshop/importPermission
    """

    url = "/mgmt/weshop/importPermission"
    with client.post(url=url, headers=headers) as r:
        return r
