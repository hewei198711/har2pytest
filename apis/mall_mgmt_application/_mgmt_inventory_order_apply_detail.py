import os

from util.client import client

params = {
    "applyId": 0,  # 申请id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_apply_detail(params=params, headers=headers):
    """
    详情修改申请
    /mgmt/inventory/order/apply/detail

    参数说明:
    - applyId: 申请id
    """

    url = "/mgmt/inventory/order/apply/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
