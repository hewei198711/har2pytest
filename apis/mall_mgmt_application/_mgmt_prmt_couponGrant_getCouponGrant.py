import os

from util.client import client

params = {
    "grantId": 0,  # grantId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getCouponGrant(params=params, headers=headers):
    """
    查询派发记录（编辑回显）
    /mgmt/prmt/couponGrant/getCouponGrant

    参数说明:
    - grantId: grantId
    """

    url = "/mgmt/prmt/couponGrant/getCouponGrant"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
