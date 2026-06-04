import os

from util.client import client

data = {
    "color": 0,  # 是否标记主题色,0:未标记; 1：已标记
    "name": "",  # 热词名称
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_saveSearchHotword(data=data, headers=headers):
    """
    新增热词
    /mgmt/cms/searchword/saveSearchHotword

    参数说明:
    - color: 是否标记主题色,0:未标记; 1：已标记
    - name: 热词名称
    - sort: 排序
    """

    url = "/mgmt/cms/searchword/saveSearchHotword"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
