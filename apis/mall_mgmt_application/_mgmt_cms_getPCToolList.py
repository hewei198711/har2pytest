import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getPCToolList(headers=headers):
    """
    获取工具列表(PC商城端)
    /mgmt/cms/getPCToolList
    """

    url = "/mgmt/cms/getPCToolList"
    with client.get(url=url, headers=headers) as r:
        return r
