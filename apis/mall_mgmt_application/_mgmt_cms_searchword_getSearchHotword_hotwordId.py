import os

from util.client import client

params = {
    "hotwordId": 0,  # hotwordId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_getSearchHotword_hotwordId(params=params, headers=headers):
    """
    根据ID查询热词
    /mgmt/cms/searchword/getSearchHotword/{hotwordId}

    参数说明:
    - hotwordId: hotwordId
    """

    url = f"/mgmt/cms/searchword/getSearchHotword/{params['hotwordId']}"
    with client.get(url=url, headers=headers) as r:
        return r
