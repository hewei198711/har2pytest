import os

from util.client import client

params = {
    "grantId": 0,  # grantId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_grantBaseInfo(params=params, headers=headers):
    """
    优惠券派发详情
    /mgmt/prmt/couponGrant/grantBaseInfo

    参数说明:
    - grantId: grantId
    """

    url = "/mgmt/prmt/couponGrant/grantBaseInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
