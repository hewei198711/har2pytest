import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getToolTitleListForMgmt(headers=headers):
    """
    获取工具PC类型标题列表
    /mgmt/cms/getToolTitleListForMgmt
    """

    url = "/mgmt/cms/getToolTitleListForMgmt"
    with client.get(url=url, headers=headers) as r:
        return r
