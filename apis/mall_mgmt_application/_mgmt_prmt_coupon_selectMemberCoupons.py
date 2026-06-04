import os

from util.client import client

params = {
    "memberId": "",  # memberId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectMemberCoupons(params=params, headers=headers):
    """
    分页获取用户优惠券（其他模块使用）
    /mgmt/prmt/coupon/selectMemberCoupons

    参数说明:
    - memberId: memberId
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/coupon/selectMemberCoupons"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
