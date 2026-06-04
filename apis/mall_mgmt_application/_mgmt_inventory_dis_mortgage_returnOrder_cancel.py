import os

from util.client import client

data = {
    "cancelRemark": "",  # 取消备注
    "id": 0,  # 押货退货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_cancel(data=data, headers=headers):
    """
    取消
    /mgmt/inventory/dis/mortgage/returnOrder/cancel

    参数说明:
    - cancelRemark: 取消备注
    - id: 押货退货单id
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
