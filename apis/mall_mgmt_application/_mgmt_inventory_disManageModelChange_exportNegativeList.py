import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_exportNegativeList(headers=headers):
    """
    导出负库存列表
    /mgmt/inventory/disManageModelChange/exportNegativeList
    """

    url = "/mgmt/inventory/disManageModelChange/exportNegativeList"
    with client.get(url=url, headers=headers) as r:
        return r
