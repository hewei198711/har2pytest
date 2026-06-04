import os

from util.client import client

params = {
    "couponIds": [],  # couponIds
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectByCouponIds(params=params, headers=headers):
    """
    根据优惠券Id批量查询返回基础对象
    /mgmt/prmt/coupon/selectByCouponIds

    参数说明:
    - couponIds: couponIds
    """

    url = "/mgmt/prmt/coupon/selectByCouponIds"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
