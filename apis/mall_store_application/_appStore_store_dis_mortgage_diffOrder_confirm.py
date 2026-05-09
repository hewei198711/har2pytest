import os

from util.client import client

data = {
    "orderId": 0,  # 货损货差单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_confirm(data=data, headers=headers):
    """
    确认收货
    /appStore/store/dis/mortgage/diffOrder/confirm

    参数说明:
    - orderId: 货损货差单id
    """

    url = "/appStore/store/dis/mortgage/diffOrder/confirm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
