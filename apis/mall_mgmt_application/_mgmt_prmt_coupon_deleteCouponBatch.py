import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_coupon_deleteCouponBatch(headers=headers):
    """
    批量删除优惠券
    /mgmt/prmt/coupon/deleteCouponBatch
    """

    url = "/mgmt/prmt/coupon/deleteCouponBatch"
    with client.post(url=url, headers=headers) as r:
        return r
