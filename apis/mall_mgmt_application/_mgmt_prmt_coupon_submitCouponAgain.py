import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_submitCouponAgain(data=data, headers=headers):
    """
    再次提交
    /mgmt/prmt/coupon/submitCouponAgain

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/coupon/submitCouponAgain"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
