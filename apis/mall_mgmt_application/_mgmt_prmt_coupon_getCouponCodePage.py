import os

from util.client import client

params = {
    "couponId": 0,  # 优惠券id
    "isExchange": 0,  # 是否已兑换1未兑换2已兑换
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "state": 0,  # 使用状态1未使用2已使用3已作废
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponCodePage(params=params, headers=headers):
    """
    优惠码分页查询
    /mgmt/prmt/coupon/getCouponCodePage

    参数说明:
    - couponId: 优惠券id
    - isExchange: 是否已兑换1未兑换2已兑换
    - pageNum: 当前页
    - pageSize: 每页条数
    - state: 使用状态1未使用2已使用3已作废
    """

    url = "/mgmt/prmt/coupon/getCouponCodePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
