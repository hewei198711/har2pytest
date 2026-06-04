import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_changeToolTitleSort(data=data, headers=headers):
    """
    按id修改工具PC类型标题排序值
    /mgmt/cms/changeToolTitleSort

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/changeToolTitleSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
