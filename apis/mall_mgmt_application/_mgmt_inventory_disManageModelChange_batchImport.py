import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_disManageModelChange_batchImport(headers=headers):
    """
    经营模式切换批量导入
    /mgmt/inventory/disManageModelChange/batchImport
    """

    url = "/mgmt/inventory/disManageModelChange/batchImport"
    with client.post(url=url, headers=headers) as r:
        return r
