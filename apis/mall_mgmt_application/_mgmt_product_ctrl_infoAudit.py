import os

from util.client import client

data = {
    "versionId": "13965",  # 版本id
    "auditResult": 1,  # 审核结果 1-通过，2-不通过
    "remarks": "同意此产品通过审核",  # 说明
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_ctrl_infoAudit(data=data, headers=headers):
    """
    产品审核商品版本
    /mgmt/product/ctrl/infoAudit

    参数说明:
    - auditResult: 审核结果 1-通过，2-不通过
    - remarks: 说明
    - versionId: 版本id
    """

    url = "/mgmt/product/ctrl/infoAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
