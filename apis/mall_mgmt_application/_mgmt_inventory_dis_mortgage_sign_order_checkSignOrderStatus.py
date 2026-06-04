import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_sign_order_checkSignOrderStatus(params=params, headers=headers):
    """
    查询签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->已取消
    /mgmt/inventory/dis/mortgage/sign/order/checkSignOrderStatus

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/dis/mortgage/sign/order/checkSignOrderStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
