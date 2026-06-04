import os

from util.client import client

data = {
    "auditStatus": 0,  # 状态 1审核通过  2审核不通过
    "id": 0,  # 主键id
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_audit(data=data, headers=headers):
    """
    审核
    /mgmt/inventory/disInventoryQuota/audit

    参数说明:
    - auditStatus: 状态 1审核通过  2审核不通过
    - id: 主键id
    - remark: 备注
    """

    url = "/mgmt/inventory/disInventoryQuota/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
