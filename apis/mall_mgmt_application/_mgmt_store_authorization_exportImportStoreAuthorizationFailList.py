import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_exportImportStoreAuthorizationFailList(headers=headers):
    """
    导出导入授权书失败列表
    /mgmt/store/authorization/exportImportStoreAuthorizationFailList
    """

    url = "/mgmt/store/authorization/exportImportStoreAuthorizationFailList"
    with client.get(url=url, headers=headers) as r:
        return r
