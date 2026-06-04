import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "id": 0,  # TODO: 添加参数说明
    "mobile": "",  # 注册手机号
    "promotionId": 0,  # 活动id
    "realName": "",  # 会员姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_addDisableUser(data=data, headers=headers):
    """
    手动新增不可参与活动顾客
    /mgmt/prmt/addDisableUser

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - promotionId: 活动id
    - realName: 会员姓名
    """

    url = "/mgmt/prmt/addDisableUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
