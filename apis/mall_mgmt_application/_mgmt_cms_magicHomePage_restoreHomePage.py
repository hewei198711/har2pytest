import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_restoreHomePage(data=data, headers=headers):
    """
    恢复魔法首页
    /mgmt/cms/magicHomePage/restoreHomePage

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/restoreHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
