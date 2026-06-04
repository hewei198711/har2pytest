import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_promoCopy_importPromoCopyLinkProduct(headers=headers):
    """
    促单词条商品列表导入
    /mgmt/cms/promoCopy/importPromoCopyLinkProduct
    """

    url = "/mgmt/cms/promoCopy/importPromoCopyLinkProduct"
    with client.post(url=url, headers=headers) as r:
        return r
