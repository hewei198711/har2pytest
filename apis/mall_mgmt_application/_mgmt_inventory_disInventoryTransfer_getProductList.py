import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_getProductList(params=params, headers=headers):
    """
    根据记录id查询转移记录的商品明细
    /mgmt/inventory/disInventoryTransfer/getProductList

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/disInventoryTransfer/getProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
