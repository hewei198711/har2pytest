import os

from util.client import client

data = {
    "continueDays": 0,  # 连续累计签到天数
    "couponId": 0,  # 优惠券id
    "couponName": "",  # 优惠券名称
    "prizeType": 0,  # 奖励内容:1-金豆,2-优惠券
    "quantity": 0,  # 奖励数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_addContinueConfig(data=data, headers=headers):
    """
    添加连续累计签到奖励配置
    /mgmt/rights/signin/addContinueConfig

    参数说明:
    - continueDays: 连续累计签到天数
    - couponId: 优惠券id
    - couponName: 优惠券名称
    - prizeType: 奖励内容:1-金豆,2-优惠券
    - quantity: 奖励数量
    """

    url = "/mgmt/rights/signin/addContinueConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
