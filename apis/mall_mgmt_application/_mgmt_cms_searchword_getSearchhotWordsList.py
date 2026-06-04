import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_getSearchhotWordsList(headers=headers):
    """
    获取热词列表
    /mgmt/cms/searchword/getSearchhotWordsList
    """

    url = "/mgmt/cms/searchword/getSearchhotWordsList"
    with client.get(url=url, headers=headers) as r:
        return r
