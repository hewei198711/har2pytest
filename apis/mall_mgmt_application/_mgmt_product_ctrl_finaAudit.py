import os

from util.client import client

data = {
    "auditResult": 0,  # 审核结果 1-通过，2-不通过
    "remarks": "",  # 说明
    "versionId": "",  # 版本id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_ctrl_finaAudit(data=data, headers=headers):
    """
    财务审核商品版本
    /mgmt/product/ctrl/finaAudit

    参数说明:
    - auditResult: 审核结果 1-通过，2-不通过
    - remarks: 说明
    - versionId: 版本id
    """

    url = "/mgmt/product/ctrl/finaAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
