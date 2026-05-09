import os

from util.client import client

params = {
    "uniqueFlagNo": "",  # uniqueFlagNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_payCheck(params=params, headers=headers):
    """
    支付前的校验:押货价有变动amountIsUpdate=true
    /appStore/store/disInventoryTransfer/payCheck

    参数说明:
    - uniqueFlagNo: uniqueFlagNo
    """

    url = "/appStore/store/disInventoryTransfer/payCheck"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
