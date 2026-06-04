import os

from util.client import client

params = {
    "grantId": 0,  # grantId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getImportMembers(params=params, headers=headers):
    """
    分页查询导入用户-优惠券派发详情
    /mgmt/prmt/couponGrant/getImportMembers

    参数说明:
    - grantId: grantId
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/couponGrant/getImportMembers"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
