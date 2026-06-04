import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_deleteImportMember(data=data, headers=headers):
    """
    删除导入的派发用户
    /mgmt/prmt/couponGrant/deleteImportMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/couponGrant/deleteImportMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
