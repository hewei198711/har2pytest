import os

from util.client import client

params = {
    "auditResult": "",  # 审核结果 1-审核通过 2-审核不通过
    "productIds": "",  # 商品id集合
    "remarks": "",  # 备注说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_batchAudit(params=params, headers=headers):
    """
    分公司价格信息批量审核
    /mgmt/product/filiale/batchAudit

    参数说明:
    - auditResult: 审核结果 1-审核通过 2-审核不通过
    - productIds: 商品id集合
    - remarks: 备注说明
    """

    url = "/mgmt/product/filiale/batchAudit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
