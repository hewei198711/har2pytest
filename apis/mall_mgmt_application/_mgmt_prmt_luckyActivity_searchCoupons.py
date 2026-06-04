import os

from util.client import client

params = {
    "couponNumber": "",  # couponNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_searchCoupons(params=params, headers=headers):
    """
    搜索优惠券
    /mgmt/prmt/luckyActivity/searchCoupons

    参数说明:
    - couponNumber: couponNumber
    """

    url = "/mgmt/prmt/luckyActivity/searchCoupons"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
