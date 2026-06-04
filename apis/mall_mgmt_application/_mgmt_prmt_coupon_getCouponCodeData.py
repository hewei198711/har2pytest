import os

from util.client import client

params = {
    "couponId": 0,  # couponId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponCodeData(params=params, headers=headers):
    """
    优惠券码数据统计
    /mgmt/prmt/coupon/getCouponCodeData

    参数说明:
    - couponId: couponId
    """

    url = "/mgmt/prmt/coupon/getCouponCodeData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
