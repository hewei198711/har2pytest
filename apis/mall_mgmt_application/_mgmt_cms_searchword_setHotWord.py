import os

from util.client import client

data = {
    "searchWord": "",  # 搜索热词
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_setHotWord(data=data, headers=headers):
    """
    设置搜索热词
    /mgmt/cms/searchword/setHotWord

    参数说明:
    - searchWord: 搜索热词
    """

    url = "/mgmt/cms/searchword/setHotWord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
