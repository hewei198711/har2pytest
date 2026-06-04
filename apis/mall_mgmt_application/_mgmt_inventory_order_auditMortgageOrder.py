import os

from util.client import client

data = {
    "auditRemarks": "",  # 审核备注
    "auditStatus": 0,  # 审核结果 0不通过 1通过
    "id": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_auditMortgageOrder(data=data, headers=headers):
    """
    运营后台审批押货单
    /mgmt/inventory/order/auditMortgageOrder

    参数说明:
    - auditRemarks: 审核备注
    - auditStatus: 审核结果 0不通过 1通过
    - id: 押货单id
    """

    url = "/mgmt/inventory/order/auditMortgageOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
