import os

from util.client import client

params = {
    "orderNo": "",  # 团购单编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_invoice_detail(params=params, headers=headers):
    """
    查询发票详情
    /mgmt/inventory/group-order/invoice/detail

    参数说明:
    - orderNo: 团购单编号
    """

    url = "/mgmt/inventory/group-order/invoice/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
