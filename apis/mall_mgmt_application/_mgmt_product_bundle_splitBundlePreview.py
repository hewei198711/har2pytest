import os

from util.client import client

params = {
    "productId": "",  # 套装id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_splitBundlePreview(params=params, headers=headers):
    """
    拆分单个套装确认页
    /mgmt/product/bundle/splitBundlePreview

    参数说明:
    - productId: 套装id
    """

    url = "/mgmt/product/bundle/splitBundlePreview"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
