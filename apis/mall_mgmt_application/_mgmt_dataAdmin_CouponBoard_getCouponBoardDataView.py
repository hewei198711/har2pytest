import os

from util.client import client

data = {
    "ids": [],  # id列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_CouponBoard_getCouponBoardDataView(data=data, headers=headers):
    """
    获取优惠券看板概览
    /mgmt/dataAdmin/CouponBoard/getCouponBoardDataView

    参数说明:
    - ids: id列表
    """

    url = "/mgmt/dataAdmin/CouponBoard/getCouponBoardDataView"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
