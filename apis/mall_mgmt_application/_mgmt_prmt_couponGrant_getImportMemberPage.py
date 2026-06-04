import os

from util.client import client

params = {
    "grantId": 0,  # grantId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "user": "",  # user
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getImportMemberPage(params=params, headers=headers):
    """
    分页查询导入用户(导入时)
    /mgmt/prmt/couponGrant/getImportMemberPage

    参数说明:
    - grantId: grantId
    - pageNum: pageNum
    - pageSize: pageSize
    - user: user
    """

    url = "/mgmt/prmt/couponGrant/getImportMemberPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
