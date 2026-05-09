import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchase_balanceAmount(headers=headers):
    """
    押货金额
    /appStore/purchase/balanceAmount
    """

    url = "/appStore/purchase/balanceAmount"
    with client.get(url=url, headers=headers) as r:
        return r
