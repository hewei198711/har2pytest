import os

from util.client import client

params = {
    "couponId": 0,  # couponId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_statisticsCouponData(params=params, headers=headers):
    """
    优惠券使用详情数据统计
    /mgmt/prmt/coupon/statisticsCouponData

    参数说明:
    - couponId: couponId
    """

    url = "/mgmt/prmt/coupon/statisticsCouponData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
