import os

from util.client import client

data = {
    "id": 0,  # id
    "sortType": 0,  # 排序类型:1.上移 2.下移 3.置顶 4.置底
    "type": 0,  # 类型:1.工具 2.标题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_changePCToolSort(data=data, headers=headers):
    """
    修改PC商城的工具排序
    /mgmt/cms/changePCToolSort

    参数说明:
    - id: id
    - sortType: 排序类型:1.上移 2.下移 3.置顶 4.置底
    - type: 类型:1.工具 2.标题
    """

    url = "/mgmt/cms/changePCToolSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
