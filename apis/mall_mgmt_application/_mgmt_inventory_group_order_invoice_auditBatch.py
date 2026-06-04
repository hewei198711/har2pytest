import os

from util.client import client

data = {
    "auditRemark": "",  # 审核备注
    "auditResult": 0,  # 审核结果 0不通过 1通过
    "ids": [],  # 审批记录id列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_invoice_auditBatch(data=data, headers=headers):
    """
    发票批量审核
    /mgmt/inventory/group-order/invoice/auditBatch

    参数说明:
    - auditRemark: 审核备注
    - auditResult: 审核结果 0不通过 1通过
    - ids: 审批记录id列表
    """

    url = "/mgmt/inventory/group-order/invoice/auditBatch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
