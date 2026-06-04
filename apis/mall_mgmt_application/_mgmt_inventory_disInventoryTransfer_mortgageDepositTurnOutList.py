import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_mortgageDepositTurnOutList(params=params, headers=headers):
    """
    1：3押货保证金转移记录
    /mgmt/inventory/disInventoryTransfer/mortgageDepositTurnOutList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disInventoryTransfer/mortgageDepositTurnOutList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
