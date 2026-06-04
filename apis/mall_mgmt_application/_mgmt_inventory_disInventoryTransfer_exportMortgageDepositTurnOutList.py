import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_exportMortgageDepositTurnOutList(params=params, headers=headers):
    """
    导出1:3押货保证金转移记录
    /mgmt/inventory/disInventoryTransfer/exportMortgageDepositTurnOutList

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/exportMortgageDepositTurnOutList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
