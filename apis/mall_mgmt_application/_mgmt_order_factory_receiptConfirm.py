import os

from util.client import client

data = {
    "id": 0,  # 返修单ID
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_receiptConfirm(data=data, headers=headers):
    """
    执行确认收货
    /mgmt/order/factory/receiptConfirm

    参数说明:
    - id: 返修单ID
    - systemCode: 查询系统编码
    """

    url = "/mgmt/order/factory/receiptConfirm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
