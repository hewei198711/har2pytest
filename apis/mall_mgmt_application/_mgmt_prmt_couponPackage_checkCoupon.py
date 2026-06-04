import os

from util.client import client

params = {
    "couponId": "",  # 优惠券id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_checkCoupon(params=params, headers=headers):
    """
    校验优惠券信息
    /mgmt/prmt/couponPackage/checkCoupon

    参数说明:
    - couponId: 优惠券id
    """

    url = "/mgmt/prmt/couponPackage/checkCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
