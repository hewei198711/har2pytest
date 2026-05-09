import os

from util.client import client

data = {
    "list": [],  # 菜单按钮id集合
    "remark": "",  # 备注
    "roleName": "",  # 角色名称
    "roleStatus": 0,  # 角色状态：0->启用；1->禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_role(data=data, headers=headers):
    """
    新增角色
    /appStore/role

    参数说明:
    - list: 菜单按钮id集合
    - remark: 备注
    - roleName: 角色名称
    - roleStatus: 角色状态：0->启用；1->禁用
    """

    url = "/appStore/role"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
