import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_whiteList_whiteListUserImport(headers=headers):
    """
    白名单用户导入
    /mgmt/cms/whiteList/whiteListUserImport
    """

    url = "/mgmt/cms/whiteList/whiteListUserImport"
    with client.post(url=url, headers=headers) as r:
        return r
