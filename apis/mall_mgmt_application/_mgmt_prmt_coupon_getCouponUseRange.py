import os

from util.client import client

params = {
    "couponId": 0,  # 优惠券id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "product": "",  # 商品编号或名称
    "promotion": "",  # 活动编号或名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponUseRange(params=params, headers=headers):
    """
    优惠券详情-使用范围-商品分页
    /mgmt/prmt/coupon/getCouponUseRange

    参数说明:
    - couponId: 优惠券id
    - pageNum: 当前页
    - pageSize: 每页条数
    - product: 商品编号或名称
    - promotion: 活动编号或名称
    """

    url = "/mgmt/prmt/coupon/getCouponUseRange"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
