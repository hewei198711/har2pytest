import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_dis_inventory_bill_printable(headers=headers):
    """
    查询库存对账单打印开关是否开启
    /appStore/dis-inventory/bill/printable
    """

    url = "/appStore/dis-inventory/bill/printable"
    with client.get(url=url, headers=headers) as r:
        return r
