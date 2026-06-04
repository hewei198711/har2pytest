import os

from util.client import client

params = {
    "couponId": 0,  # couponId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectProductPage(params=params, headers=headers):
    """
    不可用商品查询（详情）
    /mgmt/prmt/coupon/selectProductPage

    参数说明:
    - couponId: couponId
    - pageNum: pageNum
    - pageSize: pageSize
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/coupon/selectProductPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
