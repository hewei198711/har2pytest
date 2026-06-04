import os

from util.client import client

params = {
    "beginCreateTime": "",  # 开始创建时间 yyyy-MM-dd
    "bizMode": 0,  # 经营模式 1->1:3押货, 2->分级押货
    "endCreateTime": "",  # 结束创建时间 yyyy-MM-dd
    "packageName": "",  # 权限包名称
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "status": 0,  # 权限状态 1开启 2关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_permissionPackage_list(params=params, headers=headers):
    """
    列表查询
    /mgmt/store/permissionPackage/list

    参数说明:
    - beginCreateTime: 开始创建时间 yyyy-MM-dd
    - bizMode: 经营模式 1->1:3押货, 2->分级押货
    - endCreateTime: 结束创建时间 yyyy-MM-dd
    - packageName: 权限包名称
    - pageNum: 页数
    - pageSize: 页大小
    - status: 权限状态 1开启 2关闭
    """

    url = "/mgmt/store/permissionPackage/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
