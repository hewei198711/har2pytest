import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_getHomePageById(params=params, headers=headers):
    """
    根据id回显魔法首页数据
    /mgmt/cms/magicHomePage/getHomePageById

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/getHomePageById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
