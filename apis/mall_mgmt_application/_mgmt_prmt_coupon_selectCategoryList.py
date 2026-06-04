import os

from util.client import client

params = {
    "couponId": 0,  # couponId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectCategoryList(params=params, headers=headers):
    """
    查询优惠券关联的分类列表(详情)
    /mgmt/prmt/coupon/selectCategoryList

    参数说明:
    - couponId: couponId
    """

    url = "/mgmt/prmt/coupon/selectCategoryList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
