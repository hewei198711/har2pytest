import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_report_view(params=params, headers=headers):
    """
    查询分批报单明细
    /mgmt/inventory/group-order/report-view

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/inventory/group-order/report-view"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
