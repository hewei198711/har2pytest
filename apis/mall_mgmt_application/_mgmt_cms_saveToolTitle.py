import os

from util.client import client

data = {
    "sort": 0,  # 排序
    "title": "",  # PC类型标题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_saveToolTitle(data=data, headers=headers):
    """
    新增工具PC类型标题
    /mgmt/cms/saveToolTitle

    参数说明:
    - sort: 排序
    - title: PC类型标题
    """

    url = "/mgmt/cms/saveToolTitle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
