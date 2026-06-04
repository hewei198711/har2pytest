import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadImportStorePermissionTemplate(headers=headers):
    """
    下载服务中心权限导入模板
    /mgmt/store/downloadImportStorePermissionTemplate
    """

    url = "/mgmt/store/downloadImportStorePermissionTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
