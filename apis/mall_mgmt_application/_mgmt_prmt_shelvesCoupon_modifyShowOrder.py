import os

from util.client import client

data = {
    "id": 0,  # id
    "showOrder": 0,  # 展示顺序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_modifyShowOrder(data=data, headers=headers):
    """
    修改展示顺序
    /mgmt/prmt/shelvesCoupon/modifyShowOrder

    参数说明:
    - id: id
    - showOrder: 展示顺序
    """

    url = "/mgmt/prmt/shelvesCoupon/modifyShowOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
