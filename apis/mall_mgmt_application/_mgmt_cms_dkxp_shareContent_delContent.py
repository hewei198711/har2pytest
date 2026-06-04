import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_dkxp_shareContent_delContent(data=data, headers=headers):
    """
    删除代客选品分享内容
    /mgmt/cms/dkxp/shareContent/delContent

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/dkxp/shareContent/delContent"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
