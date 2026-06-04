import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_orderShareContent_delContent(data=data, headers=headers):
    """
    删除分享内容
    /mgmt/cms/orderShareContent/delContent

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/orderShareContent/delContent"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
