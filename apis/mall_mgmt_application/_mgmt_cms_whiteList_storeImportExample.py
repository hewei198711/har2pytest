import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_storeImportExample(headers=headers):
    """
    白名单服务中心导入模板
    /mgmt/cms/whiteList/storeImportExample
    """

    url = "/mgmt/cms/whiteList/storeImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
