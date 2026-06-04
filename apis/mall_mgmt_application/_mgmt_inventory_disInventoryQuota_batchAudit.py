import os

from util.client import client

data = {
    "auditStatus": 0,  # 状态 1审核通过 2审核不通过
    "ids": [],  # 需要审核的押货限额id列表
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_batchAudit(data=data, headers=headers):
    """
    批量审核
    /mgmt/inventory/disInventoryQuota/batchAudit

    参数说明:
    - auditStatus: 状态 1审核通过 2审核不通过
    - ids: 需要审核的押货限额id列表
    - remark: 备注
    """

    url = "/mgmt/inventory/disInventoryQuota/batchAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
