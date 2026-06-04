import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_detail_id(params=params, headers=headers):
    """
    押货单详情
    /mgmt/inventory/dis/mortgage/order/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/inventory/dis/mortgage/order/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
