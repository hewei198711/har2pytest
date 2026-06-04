import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_getPromoCopyLinkProductImportExample(headers=headers):
    """
    促单词条商品列表导入模板
    /mgmt/cms/promoCopy/getPromoCopyLinkProductImportExample
    """

    url = "/mgmt/cms/promoCopy/getPromoCopyLinkProductImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
