import os

from util.client import client

params = {
    "couponNumber": "",  # couponNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectCoupon(params=params, headers=headers):
    """
    根据优惠券编码搜索优惠券
    /mgmt/prmt/share/selectCoupon

    参数说明:
    - couponNumber: couponNumber
    """

    url = "/mgmt/prmt/share/selectCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
