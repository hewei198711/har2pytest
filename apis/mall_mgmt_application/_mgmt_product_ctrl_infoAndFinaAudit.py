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


def _mgmt_product_ctrl_infoAndFinaAudit(data=data, headers=headers):
    """
    产品审核商品和财务版本
    /mgmt/product/ctrl/infoAndFinaAudit

    参数说明:
    - auditResult: 审核结果 1-通过，2-不通过
    - remarks: 说明
    - versionId: 版本id
    """

    url = "/mgmt/product/ctrl/infoAndFinaAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
