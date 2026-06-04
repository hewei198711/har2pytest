import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_recordById(params=params, headers=headers):
    """
    根据id查询库存转移记录
    /mgmt/inventory/disInventoryTransfer/recordById

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/disInventoryTransfer/recordById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
