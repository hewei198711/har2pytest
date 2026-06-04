import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_userImportExample(headers=headers):
    """
    白名单用户手机号导入模板
    /mgmt/cms/whiteList/userImportExample
    """

    url = "/mgmt/cms/whiteList/userImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
