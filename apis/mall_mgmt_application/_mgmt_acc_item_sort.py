import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "sort": 0,  # 序号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_item_sort(data=data, headers=headers):
    """
    服务项目排序
    /mgmt/acc/item/sort

    参数说明:
    - sort: 序号
    """

    url = "/mgmt/acc/item/sort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
