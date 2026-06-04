import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_delete(params=params, headers=headers):
    """
    删除
    /mgmt/inventory/disInventoryQuota/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/disInventoryQuota/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
