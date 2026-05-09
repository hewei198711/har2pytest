import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_book_items(params=params, headers=headers):
    """
    查询实时库存台账明细
    /appStore/inventory/book-items

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/inventory/book-items"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
