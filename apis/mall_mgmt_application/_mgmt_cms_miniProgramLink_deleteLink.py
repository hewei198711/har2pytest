import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_miniProgramLink_deleteLink(data=data, headers=headers):
    """
    删除小程序链接
    /mgmt/cms/miniProgramLink/deleteLink

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/miniProgramLink/deleteLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
