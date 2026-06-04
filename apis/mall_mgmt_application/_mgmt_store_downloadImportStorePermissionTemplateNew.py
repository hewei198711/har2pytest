import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadImportStorePermissionTemplateNew(headers=headers):
    """
    下载服务中心权限导入模板(改版)
    /mgmt/store/downloadImportStorePermissionTemplateNew
    """

    url = "/mgmt/store/downloadImportStorePermissionTemplateNew"
    with client.get(url=url, headers=headers) as r:
        return r
