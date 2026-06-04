import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_diffOrder_getAllDiffReason(headers=headers):
    """
    获取所有货损货差详情理由
    /mgmt/inventory/diffOrder/getAllDiffReason
    """

    url = "/mgmt/inventory/diffOrder/getAllDiffReason"
    with client.get(url=url, headers=headers) as r:
        return r
