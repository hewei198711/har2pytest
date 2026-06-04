import os

from util.client import client

data = {
    "auditPass": False,  # TODO: 添加参数说明
    "auditRemark": "",  # 审核备注
    "auditResult": 0,  # 审核结果 1->通过 2->驳回
    "id": 0,  # 审核记录id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_stock_adjust_audit(data=data, headers=headers):
    """
    审核团购单调整
    /mgmt/inventory/group-order/stock/adjust/audit

    参数说明:
    - auditRemark: 审核备注
    - auditResult: 审核结果 1->通过 2->驳回
    - id: 审核记录id
    """

    url = "/mgmt/inventory/group-order/stock/adjust/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
