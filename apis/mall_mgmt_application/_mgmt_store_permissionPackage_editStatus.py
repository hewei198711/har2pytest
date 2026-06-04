import os

from util.client import client

data = {
    "id": 0,  # id
    "status": 0,  # 权限状态 1开启 2关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_permissionPackage_editStatus(data=data, headers=headers):
    """
    编辑权限包状态
    /mgmt/store/permissionPackage/editStatus

    参数说明:
    - id: id
    - status: 权限状态 1开启 2关闭
    """

    url = "/mgmt/store/permissionPackage/editStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
