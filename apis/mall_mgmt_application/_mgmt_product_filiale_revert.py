import os

from util.client import client

params = {
    "productId": "",  # 商品id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_revert(params=params, headers=headers):
    """
    分公司价格审核信息撤回
    /mgmt/product/filiale/revert

    参数说明:
    - productId: 商品id
    """

    url = "/mgmt/product/filiale/revert"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
