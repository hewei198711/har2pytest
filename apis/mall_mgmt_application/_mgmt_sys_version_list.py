import os

from util.client import client

params = {
    "clientVersion": "",  # 客户端版本号
    "pageNum": 0,  # 页码不能少于1,默认1
    "pageSize": 0,  # 显示条数不能少于1,默认10
    "platformType": 0,  # app平台：1->android,2->ios,3-鸿蒙
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_version_list(params=params, headers=headers):
    """
    分页展示版本信息
    /mgmt/sys/version/list

    参数说明:
    - clientVersion: 客户端版本号
    - pageNum: 页码不能少于1,默认1
    - pageSize: 显示条数不能少于1,默认10
    - platformType: app平台：1->android,2->ios,3-鸿蒙
    """

    url = "/mgmt/sys/version/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
