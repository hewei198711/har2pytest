import os

from util.client import client

params = {
    "couponId": 0,  # couponId
    "product": "",  # product
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_exportProductList(params=params, headers=headers):
    """
    导出优惠券关联的产品
    /mgmt/prmt/coupon/exportProductList

    参数说明:
    - couponId: couponId
    - product: product
    """

    url = "/mgmt/prmt/coupon/exportProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
