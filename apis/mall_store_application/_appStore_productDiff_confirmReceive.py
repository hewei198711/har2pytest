import os

from util.client import client

data = {
    "orderId": 0,  # 货损货差单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_confirmReceive(data=data, headers=headers):
    """
    确认收货
    /appStore/productDiff/confirmReceive

    参数说明:
    - orderId: 货损货差单id
    """

    url = "/appStore/productDiff/confirmReceive"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
