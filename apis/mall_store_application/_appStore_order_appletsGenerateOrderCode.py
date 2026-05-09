import os

from util.client import client

params = {
    "content": "",  # content
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_appletsGenerateOrderCode(params=params, headers=headers):
    """
    appletsGenerateOrderCode
    /appStore/order/appletsGenerateOrderCode

    参数说明:
    - content: content
    """

    url = "/appStore/order/appletsGenerateOrderCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
