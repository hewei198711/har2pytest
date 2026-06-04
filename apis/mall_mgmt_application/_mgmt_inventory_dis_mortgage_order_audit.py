import os

from util.client import client

data = {
    "auditRemarks": "",  # 审批备注
    "auditResult": 0,  # 审批结果 0不通过 1通过
    "orderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_audit(data=data, headers=headers):
    """
    押货单审核
    /mgmt/inventory/dis/mortgage/order/audit

    参数说明:
    - auditRemarks: 审批备注
    - auditResult: 审批结果 0不通过 1通过
    - orderId: 押货单id
    """

    url = "/mgmt/inventory/dis/mortgage/order/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
