import os

from util.client import client

data = {
    "auditRemark": "",  # 审核备注
    "auditResult": 0,  # 审核结果 0不通过 1通过
    "id": 0,  # 审批记录id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_invoice_audit(data=data, headers=headers):
    """
    发票审核
    /mgmt/inventory/group-order/invoice/audit

    参数说明:
    - auditRemark: 审核备注
    - auditResult: 审核结果 0不通过 1通过
    - id: 审批记录id
    """

    url = "/mgmt/inventory/group-order/invoice/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
