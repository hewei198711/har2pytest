import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_updatePerfectInfoSort(data=data, headers=headers):
    """
    更改完美资讯排序
    /mgmt/cms/perfectInfo/updatePerfectInfoSort

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/perfectInfo/updatePerfectInfoSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
