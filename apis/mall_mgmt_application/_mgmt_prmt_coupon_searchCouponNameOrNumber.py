import os

from util.client import client

params = {
    "couponNameOrNumber": "",  # couponNameOrNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_searchCouponNameOrNumber(params=params, headers=headers):
    """
    根据优惠券名称或者编码精确查询
    /mgmt/prmt/coupon/searchCouponNameOrNumber

    参数说明:
    - couponNameOrNumber: couponNameOrNumber
    """

    url = "/mgmt/prmt/coupon/searchCouponNameOrNumber"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
