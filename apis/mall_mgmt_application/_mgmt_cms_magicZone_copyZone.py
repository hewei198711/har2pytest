import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicZone_copyZone(data=data, headers=headers):
    """
    复制魔法专区
    /mgmt/cms/magicZone/copyZone

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicZone/copyZone"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
