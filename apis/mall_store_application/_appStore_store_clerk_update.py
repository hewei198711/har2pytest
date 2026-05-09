import os

from util.client import client

data = {
    "canLoginMall": 0,  # 允许登录商城：0->启用；1->禁用
    "canLoginStore": 0,  # 允许登录服务中心：0->启用；1->禁用
    "cardNo": "",  # 会员卡号
    "id": 0,  # 店员ID
    "loginChannel": "",  # 可登录客户端类型：1/PC，2/APP，3/小程序；多个用英文逗号分隔
    "mobile": "",  # 登录手机号码
    "name": "",  # 姓名
    "password": "",  # 登录密码
    "permission": "",  # 用户角色ID，多个用逗号分隔
    "permissionName": "",  # 用户角色名称，多个用逗号分隔
    "realname": "",  # 店员姓名
    "registerMobile": "",  # 注册手机号
    "username": "",  # 登录账号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_clerk_update(data=data, headers=headers):
    """
    修改店员账号
    /appStore/store/clerk/update

    参数说明:
    - canLoginMall: 允许登录商城：0->启用；1->禁用
    - canLoginStore: 允许登录服务中心：0->启用；1->禁用
    - cardNo: 会员卡号
    - id: 店员ID
    - loginChannel: 可登录客户端类型：1/PC，2/APP，3/小程序；多个用英文逗号分隔
    - mobile: 登录手机号码
    - name: 姓名
    - password: 登录密码
    - permission: 用户角色ID，多个用逗号分隔
    - permissionName: 用户角色名称，多个用逗号分隔
    - realname: 店员姓名
    - registerMobile: 注册手机号
    - username: 登录账号
    """

    url = "/appStore/store/clerk/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
