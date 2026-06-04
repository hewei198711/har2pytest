import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_order_detail_id(params=params, headers=headers):
    """
    获取Acc订单详情
    /mgmt/acc/order/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/acc/order/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
