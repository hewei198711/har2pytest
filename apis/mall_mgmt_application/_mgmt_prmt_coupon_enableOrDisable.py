import os

from util.client import client

data = {
    "couponState": 0,  # TODO: 添加参数说明
    "id": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_enableOrDisable(data=data, headers=headers):
    """
    优惠券停用与启用
    /mgmt/prmt/coupon/enableOrDisable
    """

    url = "/mgmt/prmt/coupon/enableOrDisable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
