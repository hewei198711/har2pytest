import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getImportStorePermissionStatus(headers=headers):
    """
    获取服务中心权限导入状态
    /mgmt/store/getImportStorePermissionStatus
    """

    url = "/mgmt/store/getImportStorePermissionStatus"
    with client.get(url=url, headers=headers) as r:
        return r
