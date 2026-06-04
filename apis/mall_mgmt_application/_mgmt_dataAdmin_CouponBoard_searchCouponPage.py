import os

from util.client import client

params = {
    "couponNameOrNumber": "",  # couponNameOrNumber
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_CouponBoard_searchCouponPage(params=params, headers=headers):
    """
    优惠券数据看板查询优惠券-分页查询
    /mgmt/dataAdmin/CouponBoard/searchCouponPage

    参数说明:
    - couponNameOrNumber: couponNameOrNumber
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/dataAdmin/CouponBoard/searchCouponPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
