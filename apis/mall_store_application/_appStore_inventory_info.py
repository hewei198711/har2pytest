import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_info(headers=headers):
    """
    库存信息
    /appStore/inventory/info
    """

    url = "/appStore/inventory/info"
    with client.get(url=url, headers=headers) as r:
        return r
