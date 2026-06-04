import os

from util.client import client

data = {
    "id": 0,  # 主键
    "showOrder": 0,  # 展示顺序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_editShowOrder(data=data, headers=headers):
    """
    修改展示顺序
    /mgmt/prmt/rights/task/editShowOrder

    参数说明:
    - id: 主键
    - showOrder: 展示顺序
    """

    url = "/mgmt/prmt/rights/task/editShowOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
