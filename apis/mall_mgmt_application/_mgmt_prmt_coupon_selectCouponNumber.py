import os

from util.client import client

params = {
    "couponNumber": "ww051901",  # couponNumber
    "couponId": "",  # couponId
}

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_coupon_selectCouponNumber(params=params, headers=headers):
    """
    查询优惠券编码是否已经存在
    /mgmt/prmt/coupon/selectCouponNumber

    参数说明:
    - couponId: couponId
    - couponNumber: couponNumber
    """

    url = "/mgmt/prmt/coupon/selectCouponNumber"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
