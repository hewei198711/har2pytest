import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_delete(data=data, headers=headers):
    """
    删除
    /mgmt/prmt/memberImport/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/memberImport/delete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
