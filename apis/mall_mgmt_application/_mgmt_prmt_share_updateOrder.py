import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "showOrder": 0,  # 展示顺序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_updateOrder(data=data, headers=headers):
    """
    修改展示顺序
    /mgmt/prmt/share/updateOrder

    参数说明:
    - showOrder: 展示顺序
    """

    url = "/mgmt/prmt/share/updateOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
