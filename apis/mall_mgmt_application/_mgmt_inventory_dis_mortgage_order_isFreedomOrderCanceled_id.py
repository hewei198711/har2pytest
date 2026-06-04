import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_isFreedomOrderCanceled_id(params=params, headers=headers):
    """
    查询随心购押货单对应商城订单是否已取消
    /mgmt/inventory/dis/mortgage/order/isFreedomOrderCanceled/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/inventory/dis/mortgage/order/isFreedomOrderCanceled/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
