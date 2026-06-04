import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_deepDeleteHomePage(data=data, headers=headers):
    """
    深度删除魔法首页
    /mgmt/cms/magicHomePage/deepDeleteHomePage

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/deepDeleteHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
