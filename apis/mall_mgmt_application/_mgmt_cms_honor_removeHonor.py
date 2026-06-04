import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_removeHonor(data=data, headers=headers):
    """
    删除用户荣誉
    /mgmt/cms/honor/removeHonor

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/honor/removeHonor"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
