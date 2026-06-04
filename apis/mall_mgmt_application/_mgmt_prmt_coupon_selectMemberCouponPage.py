import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectMemberCouponPage(params=params, headers=headers):
    """
    分页查询当前用户优惠券
    /mgmt/prmt/coupon/selectMemberCouponPage

    参数说明:
    - cardNo: cardNo
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/coupon/selectMemberCouponPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
