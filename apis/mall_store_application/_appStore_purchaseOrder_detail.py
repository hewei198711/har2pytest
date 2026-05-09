import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_detail(headers=headers):
    """
    押货单详情
    /appStore/purchaseOrder/detail
    """

    url = "/appStore/purchaseOrder/detail"
    with client.get(url=url, headers=headers) as r:
        return r
