import os

from util.client import client

data = {
    "ids": [],  # 用户优惠券id
    "invalidReason": "",  # 作废原因
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_batchInvalidCoupon(data=data, headers=headers):
    """
    批量作废优惠券
    /mgmt/prmt/coupon/batchInvalidCoupon

    参数说明:
    - ids: 用户优惠券id
    - invalidReason: 作废原因
    """

    url = "/mgmt/prmt/coupon/batchInvalidCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
