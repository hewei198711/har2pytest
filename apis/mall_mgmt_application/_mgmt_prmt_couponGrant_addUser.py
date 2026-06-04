import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "code": "",  # 使用门店
    "couponId": 0,  # 优惠券id
    "everyCount": 0,  # 派发数量
    "grantId": 0,  # 派发id
    "mobile": "",  # 注册手机号
    "realName": "",  # 会员姓名
    "type": 0,  # 派发方式1等量2按需
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_addUser(data=data, headers=headers):
    """
    手动新增派发顾客
    /mgmt/prmt/couponGrant/addUser

    参数说明:
    - cardNo: 会员卡号
    - code: 使用门店
    - couponId: 优惠券id
    - everyCount: 派发数量
    - grantId: 派发id
    - mobile: 注册手机号
    - realName: 会员姓名
    - type: 派发方式1等量2按需
    """

    url = "/mgmt/prmt/couponGrant/addUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
