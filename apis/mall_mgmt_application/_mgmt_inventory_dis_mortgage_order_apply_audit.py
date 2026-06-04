import os

from util.client import client

data = {
    "auditRemarks": "",  # 修改说明
    "auditStatus": 0,  # 审批状态 0驳回 1同意
    "id": 0,  # 押货单申请id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_apply_audit(data=data, headers=headers):
    """
    审核
    /mgmt/inventory/dis/mortgage/order/apply/audit

    参数说明:
    - auditRemarks: 修改说明
    - auditStatus: 审批状态 0驳回 1同意
    - id: 押货单申请id
    """

    url = "/mgmt/inventory/dis/mortgage/order/apply/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
