import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listImportStorePermissionNew(params=params, headers=headers):
    """
    分页查询导入服务中心权限(改版)
    /mgmt/store/listImportStorePermissionNew

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/mgmt/store/listImportStorePermissionNew"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
