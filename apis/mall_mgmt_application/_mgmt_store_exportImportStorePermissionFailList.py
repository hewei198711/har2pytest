import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportImportStorePermissionFailList(headers=headers):
    """
    导出导入服务中心权限失败列表
    /mgmt/store/exportImportStorePermissionFailList
    """

    url = "/mgmt/store/exportImportStorePermissionFailList"
    with client.get(url=url, headers=headers) as r:
        return r
