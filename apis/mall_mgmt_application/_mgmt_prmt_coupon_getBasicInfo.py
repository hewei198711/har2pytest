import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getBasicInfo(params=params, headers=headers):
    """
    优惠券详情-基础信息
    /mgmt/prmt/coupon/getBasicInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/coupon/getBasicInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
