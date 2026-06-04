import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getCatalogList(headers=headers):
    """
    获取商品分类
    /mgmt/cms/getCatalogList
    """

    url = "/mgmt/cms/getCatalogList"
    with client.get(url=url, headers=headers) as r:
        return r
