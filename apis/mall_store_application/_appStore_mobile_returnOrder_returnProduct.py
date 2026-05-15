import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_returnOrder_returnProduct(headers=headers):
    """
    押货退货商品
    /appStore/mobile/returnOrder/returnProduct
    """

    url = "/appStore/mobile/returnOrder/returnProduct"
    with client.get(url=url, headers=headers) as r:
        return r
