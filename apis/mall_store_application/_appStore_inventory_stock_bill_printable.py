import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_stock_bill_printable(headers=headers):
    """
    查询库存对账单打印开关是否开启
    /appStore/inventory/stock-bill-printable
    """

    url = "/appStore/inventory/stock-bill-printable"
    with client.get(url=url, headers=headers) as r:
        return r
