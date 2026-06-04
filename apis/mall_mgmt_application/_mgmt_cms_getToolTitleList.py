import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getToolTitleList(headers=headers):
    """
    获取工具PC类型标题列表(已启用)
    /mgmt/cms/getToolTitleList
    """

    url = "/mgmt/cms/getToolTitleList"
    with client.get(url=url, headers=headers) as r:
        return r
