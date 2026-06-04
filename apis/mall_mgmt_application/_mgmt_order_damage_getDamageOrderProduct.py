import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_damage_getDamageOrderProduct(params=params, headers=headers):
    """
    获取货损货差的订单及商品信息
    /mgmt/order/damage/getDamageOrderProduct

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/order/damage/getDamageOrderProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
