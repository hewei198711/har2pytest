import os

from util.client import client

data = {
    "bizMode": 0,  # 经营模式 1->1:3押货, 2->分级押货
    "oneThreeMode": False,  # TODO: 添加参数说明
    "opSwitch": False,  # TODO: 添加参数说明
    "opType": 0,  # 操作 1替换 2新增
    "permissions": [],  # 权限列表
    "storeCodes": [],  # 店铺编号列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_importStorePermissionNew(data=data, headers=headers):
    """
    导入服务中心权限(改版)
    /mgmt/store/importStorePermissionNew

    参数说明:
    - bizMode: 经营模式 1->1:3押货, 2->分级押货
    - opType: 操作 1替换 2新增
    - permissions: 权限列表
    - storeCodes: 店铺编号列表
    """

    url = "/mgmt/store/importStorePermissionNew"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
