import os

from util.client import client

params = {
    "productIds": [],  # productIds
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_splitPreview(params=params, headers=headers):
    """
    批量/单独拆分前明细预览
    /mgmt/product/bundle/splitPreview

    参数说明:
    - productIds: productIds
    """

    url = "/mgmt/product/bundle/splitPreview"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
