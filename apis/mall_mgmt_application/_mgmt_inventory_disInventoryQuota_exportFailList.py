import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_exportFailList(headers=headers):
    """
    库存限额失败记录
    /mgmt/inventory/disInventoryQuota/exportFailList
    """

    url = "/mgmt/inventory/disInventoryQuota/exportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
