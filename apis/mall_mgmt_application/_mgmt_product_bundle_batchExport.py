import os

from util.client import client

params = {
    "productIds": [],  # productIds
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_batchExport(params=params, headers=headers):
    """
    调整明细导出
    /mgmt/product/bundle/batchExport

    参数说明:
    - productIds: productIds
    """

    url = "/mgmt/product/bundle/batchExport"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
