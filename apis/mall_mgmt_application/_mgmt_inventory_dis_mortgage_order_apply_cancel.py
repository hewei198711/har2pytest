import os

from util.client import client

data = {
    "applyId": 0,  # 申请id
    "storeCode": "",  # 服务中心编号,不需填写
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_apply_cancel(data=data, headers=headers):
    """
    取消
    /mgmt/inventory/dis/mortgage/order/apply/cancel

    参数说明:
    - applyId: 申请id
    - storeCode: 服务中心编号,不需填写
    """

    url = "/mgmt/inventory/dis/mortgage/order/apply/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
