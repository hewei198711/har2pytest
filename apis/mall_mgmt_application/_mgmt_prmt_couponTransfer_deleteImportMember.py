import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_deleteImportMember(data=data, headers=headers):
    """
    清空导入列表
    /mgmt/prmt/couponTransfer/deleteImportMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/couponTransfer/deleteImportMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
