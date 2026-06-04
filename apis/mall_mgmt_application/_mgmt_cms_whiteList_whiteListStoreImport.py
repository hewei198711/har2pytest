import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_whiteList_whiteListStoreImport(headers=headers):
    """
    白名单服务中心导入
    /mgmt/cms/whiteList/whiteListStoreImport
    """

    url = "/mgmt/cms/whiteList/whiteListStoreImport"
    with client.post(url=url, headers=headers) as r:
        return r
