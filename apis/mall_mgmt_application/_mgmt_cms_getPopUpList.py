import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getPopUpList(headers=headers):
    """
    获取弹窗配置列表
    /mgmt/cms/getPopUpList
    """

    url = "/mgmt/cms/getPopUpList"
    with client.get(url=url, headers=headers) as r:
        return r
