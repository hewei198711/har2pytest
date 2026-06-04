import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_whiteList_removeAllWhiteListStore(headers=headers):
    """
    清空白名单服务中心列表
    /mgmt/cms/whiteList/removeAllWhiteListStore
    """

    url = "/mgmt/cms/whiteList/removeAllWhiteListStore"
    with client.post(url=url, headers=headers) as r:
        return r
