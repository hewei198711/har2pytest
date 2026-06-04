import os

from util.client import client

params = {
    "couponId": 0,  # couponId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_exportPromotionList(params=params, headers=headers):
    """
    优惠券关联的活动列表导出
    /mgmt/prmt/coupon/exportPromotionList

    参数说明:
    - couponId: couponId
    """

    url = "/mgmt/prmt/coupon/exportPromotionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
