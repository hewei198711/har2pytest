import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_checkIsAuditAmountOverLimit(params=params, headers=headers):
    """
    查询押货单是否超出库存限额
    /mgmt/inventory/dis/mortgage/order/checkIsAuditAmountOverLimit

    参数说明:
    - orderId: orderId
    """

    url = "/mgmt/inventory/dis/mortgage/order/checkIsAuditAmountOverLimit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
