import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_remit_batchImportFor13(headers=headers):
    """
    1:3手工录入流水批量导入
    /mgmt/inventory/remit/batchImportFor13
    """

    url = "/mgmt/inventory/remit/batchImportFor13"
    with client.post(url=url, headers=headers) as r:
        return r
