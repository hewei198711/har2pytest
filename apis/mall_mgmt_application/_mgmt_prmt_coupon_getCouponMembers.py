import os

from util.client import client

params = {
    "couponId": 0,  # couponId
    "ids": [],  # ids
    "memberInfo": "",  # memberInfo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponMembers(params=params, headers=headers):
    """
    导出有券顾客列表
    /mgmt/prmt/coupon/getCouponMembers

    参数说明:
    - couponId: couponId
    - ids: ids
    - memberInfo: memberInfo
    """

    url = "/mgmt/prmt/coupon/getCouponMembers"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
