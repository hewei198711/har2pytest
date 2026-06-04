import os

from util.client import client

data = {
    "id": 0,  # id
    "removeRemark": "",  # 跟进结果
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_removeOrderNoarrivewarn(data=data, headers=headers):
    """
    解除订单货物未送达预警
    /mgmt/order/removeOrderNoarrivewarn

    参数说明:
    - id: id
    - removeRemark: 跟进结果
    """

    url = "/mgmt/order/removeOrderNoarrivewarn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
