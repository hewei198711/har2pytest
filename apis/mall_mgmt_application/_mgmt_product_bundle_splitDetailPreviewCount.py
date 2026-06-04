import os

from util.client import client

params = {
    "productId": 0,  # productId
    "splitId": "",  # 拆分id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_splitDetailPreviewCount(params=params, headers=headers):
    """
    拆分明细数量统计--拆分结果预览
    /mgmt/product/bundle/splitDetailPreviewCount

    参数说明:
    - productId: productId
    - splitId: 拆分id
    """

    url = "/mgmt/product/bundle/splitDetailPreviewCount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
