import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_deleteCouponProductDisable(data=data, headers=headers):
    """
    删除优惠券关联的不可用商品(详情)
    /mgmt/prmt/coupon/deleteCouponProductDisable

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/coupon/deleteCouponProductDisable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
