import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_getReason(headers=headers):
    """
    获取各种退换货原因
    /appStore/purchaseReturnOrder/getReason
    """

    url = "/appStore/purchaseReturnOrder/getReason"
    with client.get(url=url, headers=headers) as r:
        return r
