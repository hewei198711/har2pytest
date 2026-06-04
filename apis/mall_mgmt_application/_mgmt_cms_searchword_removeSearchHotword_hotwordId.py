import os

from util.client import client

params = {
    "hotwordId": 0,  # hotwordId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_removeSearchHotword_hotwordId(params=params, headers=headers):
    """
    删除热词
    /mgmt/cms/searchword/removeSearchHotword/{hotwordId}

    参数说明:
    - hotwordId: hotwordId
    """

    url = f"/mgmt/cms/searchword/removeSearchHotword/{params['hotwordId']}"
    with client.get(url=url, headers=headers) as r:
        return r
