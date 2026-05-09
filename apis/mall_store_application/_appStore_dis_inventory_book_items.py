import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_dis_inventory_book_items(params=params, headers=headers):
    """
    查询实时库存台账明细
    /appStore/dis-inventory/book-items

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/dis-inventory/book-items"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
