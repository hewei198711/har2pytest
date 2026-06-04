import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_reUpload(data=data, headers=headers):
    """
    重试
    /mgmt/prmt/memberImport/reUpload

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/memberImport/reUpload"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
