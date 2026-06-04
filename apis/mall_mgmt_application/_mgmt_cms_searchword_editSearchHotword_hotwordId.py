import os

from util.client import client

params = {
    "hotwordId": 0,  # hotwordId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_editSearchHotword_hotwordId(params=params, headers=headers):
    """
    编辑热词
    /mgmt/cms/searchword/editSearchHotword/{hotwordId}

    参数说明:
    - hotwordId: hotwordId
    - color: 是否标记主题色,0:未标记; 1：已标记
    - name: 热词名称
    - sort: 排序
    """

    url = f"/mgmt/cms/searchword/editSearchHotword/{params['hotwordId']}"
    with client.get(url=url, headers=headers) as r:
        return r
