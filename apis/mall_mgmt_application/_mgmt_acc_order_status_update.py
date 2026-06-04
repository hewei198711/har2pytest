import os

from util.client import client

data = {
    "accOrderId": 0,  # 服务单Id
    "orderStatus": 0,  # 状态 -1：已取消 0：待接单（默认）1：待服务 2：已完成
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_order_status_update(data=data, headers=headers):
    """
    变更服务单状态
    /mgmt/acc/order/status/update

    参数说明:
    - accOrderId: 服务单Id
    - orderStatus: 状态 -1：已取消 0：待接单（默认）1：待服务 2：已完成
    - remarks: 备注
    """

    url = "/mgmt/acc/order/status/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
