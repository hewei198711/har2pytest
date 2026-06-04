import os

from util.client import client

data = {
    "id": 0,  # id
    "sortType": 0,  # 排序类型:1.上移 2.下移 3.置顶 4.置底
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_typeLabel_changeTypeLabelSort(data=data, headers=headers):
    """
    修改素材分类排序
    /mgmt/cms/typeLabel/changeTypeLabelSort

    参数说明:
    - id: id
    - sortType: 排序类型:1.上移 2.下移 3.置顶 4.置底
    """

    url = "/mgmt/cms/typeLabel/changeTypeLabelSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
