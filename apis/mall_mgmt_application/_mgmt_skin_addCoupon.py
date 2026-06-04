import os

from util.client import client

data = {
    "addTime": "",  # 添加时间
    "couponCode": "",  # 优惠券编码
    "couponCount": 0,  # 优惠券总量
    "couponName": "",  # 名称
    "couponType": 0,  # 类型
    "faceValue": 0.0,  # 面额
    "limitCount": 0,  # 最大可获得数量
    "startTime": "",  # 生效时间
    "usageRules": "",  # 使用规则
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_skin_addCoupon(data=data, headers=headers):
    """
    新增优惠券
    /mgmt/skin/addCoupon

    参数说明:
    - addTime: 添加时间
    - couponCode: 优惠券编码
    - couponCount: 优惠券总量
    - couponName: 名称
    - couponType: 类型
    - faceValue: 面额
    - limitCount: 最大可获得数量
    - startTime: 生效时间
    - usageRules: 使用规则
    """

    url = "/mgmt/skin/addCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
