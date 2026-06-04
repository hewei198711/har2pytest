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


def _mgmt_order_factory_cancelFactoryOrder(data=data, headers=headers):
    """
    取消返修单
    /mgmt/order/factory/cancelFactoryOrder

    参数说明:
    - id: 返修单ID
    - systemCode: 查询系统编码
    """

    url = "/mgmt/order/factory/cancelFactoryOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
