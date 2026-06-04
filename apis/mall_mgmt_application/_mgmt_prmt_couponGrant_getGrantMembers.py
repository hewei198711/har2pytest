import os

from util.client import client

params = {
    "grantId": 0,  # grantId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getGrantMembers(params=params, headers=headers):
    """
    导出派发派发用户
    /mgmt/prmt/couponGrant/getGrantMembers

    参数说明:
    - grantId: grantId
    """

    url = "/mgmt/prmt/couponGrant/getGrantMembers"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
