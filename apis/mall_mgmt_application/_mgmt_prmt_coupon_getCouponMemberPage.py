import os

from util.client import client

params = {
    "couponId": 0,  # couponId
    "memberInfo": "",  # memberInfo
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponMemberPage(params=params, headers=headers):
    """
    分页查询有券用户列表
    /mgmt/prmt/coupon/getCouponMemberPage

    参数说明:
    - couponId: couponId
    - memberInfo: memberInfo
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/coupon/getCouponMemberPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
