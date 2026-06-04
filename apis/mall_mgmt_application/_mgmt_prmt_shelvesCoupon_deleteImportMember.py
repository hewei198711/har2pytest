import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_deleteImportMember(data=data, headers=headers):
    """
    删除导入上架对象
    /mgmt/prmt/shelvesCoupon/deleteImportMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/shelvesCoupon/deleteImportMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
