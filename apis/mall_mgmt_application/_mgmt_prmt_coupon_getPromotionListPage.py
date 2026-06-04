import os

from util.client import client

params = {
    "couponId": 0,  # couponId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getPromotionListPage(params=params, headers=headers):
    """
    分页获取优惠券关联的活动列表（详情）
    /mgmt/prmt/coupon/getPromotionListPage

    参数说明:
    - couponId: couponId
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/coupon/getPromotionListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
