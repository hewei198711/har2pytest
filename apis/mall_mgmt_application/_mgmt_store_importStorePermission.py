import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importStorePermission(headers=headers):
    """
    导入服务中心权限
    /mgmt/store/importStorePermission
    """

    url = "/mgmt/store/importStorePermission"
    with client.post(url=url, headers=headers) as r:
        return r
