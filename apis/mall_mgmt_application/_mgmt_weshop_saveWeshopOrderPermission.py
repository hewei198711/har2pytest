import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "exTime": "",  # 限制时间截止至
    "phone": "",  # 注册手机号码
    "realname": "",  # 姓名
    "type": "",  # 类型，两个值中间用,分隔
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_saveWeshopOrderPermission(data=data, headers=headers):
    """
    新增KOS转分权限
    /mgmt/weshop/saveWeshopOrderPermission

    参数说明:
    - cardNo: 会员卡号
    - exTime: 限制时间截止至
    - phone: 注册手机号码
    - realname: 姓名
    - type: 类型，两个值中间用,分隔
    """

    url = "/mgmt/weshop/saveWeshopOrderPermission"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
