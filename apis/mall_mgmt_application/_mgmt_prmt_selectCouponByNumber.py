import os

from util.client import client

params = {
    "couponNumber": "",  # couponNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_selectCouponByNumber(params=params, headers=headers):
    """
    根据优惠券编码查询优惠券（新建活动）
    /mgmt/prmt/selectCouponByNumber

    参数说明:
    - couponNumber: couponNumber
    """

    url = "/mgmt/prmt/selectCouponByNumber"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
