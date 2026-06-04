import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_bill_print_switch_history(params=params, headers=headers):
    """
    查询库存对账单打印开关历史记录
    /mgmt/inventory/bill/print-switch-history

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/mgmt/inventory/bill/print-switch-history"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
