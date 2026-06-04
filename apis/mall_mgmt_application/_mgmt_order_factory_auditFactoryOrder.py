import os

from util.client import client

data = {
    "auditRemark": "",  # 审核说明
    "id": 0,  # 返修单ID
    "orderStatus": 0,  # 返修单状态：1->同意；2->驳回；
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_auditFactoryOrder(data=data, headers=headers):
    """
    执行返修单审核
    /mgmt/order/factory/auditFactoryOrder

    参数说明:
    - auditRemark: 审核说明
    - id: 返修单ID
    - orderStatus: 返修单状态：1->同意；2->驳回；
    """

    url = "/mgmt/order/factory/auditFactoryOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
