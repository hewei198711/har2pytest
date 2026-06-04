import os

from util.client import client

params = {
    "auditResult": "",  # 审核结果 1-审核通过 2-审核不通过
    "productId": "",  # 商品id
    "remarks": "",  # 备注说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_audit(params=params, headers=headers):
    """
    分公司价格信息审核
    /mgmt/product/filiale/audit

    参数说明:
    - auditResult: 审核结果 1-审核通过 2-审核不通过
    - productId: 商品id
    - remarks: 备注说明
    """

    url = "/mgmt/product/filiale/audit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
