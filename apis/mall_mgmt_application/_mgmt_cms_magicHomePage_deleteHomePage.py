import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_deleteHomePage(data=data, headers=headers):
    """
    删除魔法首页
    /mgmt/cms/magicHomePage/deleteHomePage

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/deleteHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
