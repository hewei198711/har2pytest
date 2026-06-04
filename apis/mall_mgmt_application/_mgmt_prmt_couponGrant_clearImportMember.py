import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_couponGrant_clearImportMember(headers=headers):
    """
    清除缓存里导入的派发用户
    /mgmt/prmt/couponGrant/clearImportMember
    """

    url = "/mgmt/prmt/couponGrant/clearImportMember"
    with client.post(url=url, headers=headers) as r:
        return r
