import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_bill_print_switch_opened(headers=headers):
    """
    查询库存对账单打印开关是否开启
    /mgmt/dis-inventory/bill/print-switch-opened
    """

    url = "/mgmt/dis-inventory/bill/print-switch-opened"
    with client.get(url=url, headers=headers) as r:
        return r
