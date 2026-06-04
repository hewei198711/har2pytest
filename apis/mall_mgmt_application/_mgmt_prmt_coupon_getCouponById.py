import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponById(params=params, headers=headers):
    """
    根据id查询优惠券（用于编辑）
    /mgmt/prmt/coupon/getCouponById

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/coupon/getCouponById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
