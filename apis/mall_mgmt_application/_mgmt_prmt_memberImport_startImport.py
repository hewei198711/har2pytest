import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_startImport(data=data, headers=headers):
    """
    开始导入
    /mgmt/prmt/memberImport/startImport

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/memberImport/startImport"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
