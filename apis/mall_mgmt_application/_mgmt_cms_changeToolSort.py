import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_changeToolSort(data=data, headers=headers):
    """
    按id修改工具排序值
    /mgmt/cms/changeToolSort

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/changeToolSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
