import os

from util.client import client

data = {
    "ids": [],  # id列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_CouponBoard_getCouponBoardProvinceTopList(data=data, headers=headers):
    """
    获取优惠券看板省份TOP10
    /mgmt/dataAdmin/CouponBoard/getCouponBoardProvinceTopList

    参数说明:
    - ids: id列表
    """

    url = "/mgmt/dataAdmin/CouponBoard/getCouponBoardProvinceTopList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
