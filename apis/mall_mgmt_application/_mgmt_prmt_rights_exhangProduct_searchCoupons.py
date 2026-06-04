import os

from util.client import client

params = {
    "couponNumber": "",  # couponNumber
    "isAccurateSearch": 0,  # isAccurateSearch
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_searchCoupons(params=params, headers=headers):
    """
    搜索优惠券
    /mgmt/prmt/rights/exhangProduct/searchCoupons

    参数说明:
    - couponNumber: couponNumber
    - isAccurateSearch: isAccurateSearch
    """

    url = "/mgmt/prmt/rights/exhangProduct/searchCoupons"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
