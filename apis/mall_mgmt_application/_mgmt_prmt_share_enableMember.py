import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_enableMember(data=data, headers=headers):
    """
    启用
    /mgmt/prmt/share/enableMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/share/enableMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
