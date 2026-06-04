import os

from util.client import client

params = {
    "memberId": 0,  # memberId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectMemberCouponLists(params=params, headers=headers):
    """
    获取用户所有优惠券列表
    /mgmt/prmt/coupon/selectMemberCouponLists

    参数说明:
    - memberId: memberId
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/coupon/selectMemberCouponLists"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
