import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "roleName": "",  # 角色名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_role_page(params=params, headers=headers):
    """
    角色分页列表
    /appStore/role/page

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - roleName: 角色名称
    """

    url = "/appStore/role/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
