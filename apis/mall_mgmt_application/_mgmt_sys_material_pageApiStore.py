import os

from util.client import client

params = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页大小
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_pageApiStore(params=params, headers=headers):
    """
    分页查询服务中心列表（只返回基本信息）
    /mgmt/sys/material/pageApiStore

    参数说明:
    - pageNum: 页码
    - pageSize: 每页大小
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/sys/material/pageApiStore"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
