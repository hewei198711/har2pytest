import os

from util.client import client

params = {
    "id": 0,  # 批量导入记录id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getImportStorePermissionFailListNew(params=params, headers=headers):
    """
    获取导入服务中心权限失败列表(改版)
    /mgmt/store/getImportStorePermissionFailListNew

    参数说明:
    - id: 批量导入记录id
    """

    url = "/mgmt/store/getImportStorePermissionFailListNew"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
