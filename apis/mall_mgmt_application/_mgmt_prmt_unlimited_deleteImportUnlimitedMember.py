import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_unlimited_deleteImportUnlimitedMember(data=data, headers=headers):
    """
    清空不受限制活动顾客（活动id）
    /mgmt/prmt/unlimited/deleteImportUnlimitedMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/unlimited/deleteImportUnlimitedMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
