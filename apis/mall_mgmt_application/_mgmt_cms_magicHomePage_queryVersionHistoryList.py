import os

from util.client import client

params = {
    "versionLinkId": 0,  # versionLinkId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_queryVersionHistoryList(params=params, headers=headers):
    """
    获取魔法首页版本历史列表
    /mgmt/cms/magicHomePage/queryVersionHistoryList

    参数说明:
    - versionLinkId: versionLinkId
    """

    url = "/mgmt/cms/magicHomePage/queryVersionHistoryList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
