import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_diffOrder_dealReceiveDiffOrder(headers=headers):
    """
    手动处理超时未收货的货损货差单
    /mgmt/inventory/diffOrder/dealReceiveDiffOrder
    """

    url = "/mgmt/inventory/diffOrder/dealReceiveDiffOrder"
    with client.post(url=url, headers=headers) as r:
        return r
