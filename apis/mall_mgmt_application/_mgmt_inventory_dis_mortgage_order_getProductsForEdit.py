import os

from util.client import client

params = {
    "orderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_getProductsForEdit(params=params, headers=headers):
    """
    编辑押货单时查询最新的商品列表
    /mgmt/inventory/dis/mortgage/order/getProductsForEdit

    参数说明:
    - orderId: 押货单id
    """

    url = "/mgmt/inventory/dis/mortgage/order/getProductsForEdit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
