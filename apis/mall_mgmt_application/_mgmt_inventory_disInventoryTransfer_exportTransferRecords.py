import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_exportTransferRecords(params=params, headers=headers):
    """
    导出1:3库存转移记录
    /mgmt/inventory/disInventoryTransfer/exportTransferRecords

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/exportTransferRecords"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
