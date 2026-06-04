import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_diffOrder_syncAllOrderFromWorkPlatform(headers=headers):
    """
    手动同步工作平台待审核货损货差单
    /mgmt/inventory/diffOrder/syncAllOrderFromWorkPlatform
    """

    url = "/mgmt/inventory/diffOrder/syncAllOrderFromWorkPlatform"
    with client.post(url=url, headers=headers) as r:
        return r
