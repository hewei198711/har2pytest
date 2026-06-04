import os

from util.client import client

data = {
    "bizMode": 0,  # 经营模式 1->1:3押货, 2->分级押货
    "id": 0,  # id
    "packageName": "",  # 权限包名称
    "permissions": [],  # 权限列表
    "status": 0,  # 权限状态 1开启 2关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_permissionPackage_add(data=data, headers=headers):
    """
    添加权限包
    /mgmt/store/permissionPackage/add

    参数说明:
    - bizMode: 经营模式 1->1:3押货, 2->分级押货
    - id: id
    - packageName: 权限包名称
    - permissions: 权限列表
    - status: 权限状态 1开启 2关闭
    """

    url = "/mgmt/store/permissionPackage/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
