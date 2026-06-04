import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_fetchPieceBoxCostCeiling(headers=headers):
    """
    获取启用中的拼箱费上限
    /mgmt/inventory/dis/mortgage/order/fetchPieceBoxCostCeiling
    """

    url = "/mgmt/inventory/dis/mortgage/order/fetchPieceBoxCostCeiling"
    with client.get(url=url, headers=headers) as r:
        return r
