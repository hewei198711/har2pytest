import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_deleteImport(data=data, headers=headers):
    """
    删除导入内容
    /mgmt/prmt/memberImport/deleteImport

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/memberImport/deleteImport"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
