import os

from util.client import client

params = {
    "couponNameOrNumber": "",  # couponNameOrNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_complex_selectGrantCoupon(params=params, headers=headers):
    """
    搜索签约购4.0活动派发的优惠券
    /mgmt/prmt/complex/selectGrantCoupon

    参数说明:
    - couponNameOrNumber: couponNameOrNumber
    """

    url = "/mgmt/prmt/complex/selectGrantCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
