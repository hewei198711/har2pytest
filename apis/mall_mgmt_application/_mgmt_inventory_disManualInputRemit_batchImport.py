import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_disManualInputRemit_batchImport(headers=headers):
    """
    85折手工录入流水批量导入
    /mgmt/inventory/disManualInputRemit/batchImport
    """

    url = "/mgmt/inventory/disManualInputRemit/batchImport"
    with client.post(url=url, headers=headers) as r:
        return r
