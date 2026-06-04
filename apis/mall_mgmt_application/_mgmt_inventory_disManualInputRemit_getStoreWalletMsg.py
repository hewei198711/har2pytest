import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_getStoreWalletMsg(params=params, headers=headers):
    """
    1:3押货余额及85折保证金余额查询
    /mgmt/inventory/disManualInputRemit/getStoreWalletMsg

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/disManualInputRemit/getStoreWalletMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
