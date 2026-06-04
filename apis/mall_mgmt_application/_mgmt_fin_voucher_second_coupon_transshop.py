import os

from util.client import client

data = {
    "platformType": 0,  # 平台类型，前端无需传递此参数
    "secondCouponIdList": [],  # 秒返券id集合
    "targetShopCode": "",  # 转入服务中心编码
    "targetShopName": "",  # 转入服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_transshop(data=data, headers=headers):
    """
    秒返券转店
    /mgmt/fin/voucher/second/coupon/transshop

    参数说明:
    - platformType: 平台类型，前端无需传递此参数
    - secondCouponIdList: 秒返券id集合
    - targetShopCode: 转入服务中心编码
    - targetShopName: 转入服务中心名称
    """

    url = "/mgmt/fin/voucher/second/coupon/transshop"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
