import os

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_addCouponProduct(data=data, headers=headers):
    """
    添加优惠券关联的可用商品(详情)
    /mgmt/prmt/coupon/addCouponProduct

    参数说明:
    - couponId: 优惠券id
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/coupon/addCouponProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
