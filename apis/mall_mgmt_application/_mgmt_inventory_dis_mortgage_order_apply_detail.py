import os

from util.client import client

params = {
    "applyId": 0,  # 申请id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_apply_detail(params=params, headers=headers):
    """
    详情
    /mgmt/inventory/dis/mortgage/order/apply/detail

    参数说明:
    - applyId: 申请id
    """

    url = "/mgmt/inventory/dis/mortgage/order/apply/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
