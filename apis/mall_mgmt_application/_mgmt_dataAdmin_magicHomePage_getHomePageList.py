import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_magicHomePage_getHomePageList(headers=headers):
    """
    查询魔法首页列表(下拉框)
    /mgmt/dataAdmin/magicHomePage/getHomePageList
    """

    url = "/mgmt/dataAdmin/magicHomePage/getHomePageList"
    with client.get(url=url, headers=headers) as r:
        return r
