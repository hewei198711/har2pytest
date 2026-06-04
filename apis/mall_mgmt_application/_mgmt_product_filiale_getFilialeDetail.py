import os

from util.client import client

params = {
    "productId": "",  # 商品id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_getFilialeDetail(params=params, headers=headers):
    """
    分公司价格信息详情
    /mgmt/product/filiale/getFilialeDetail

    参数说明:
    - productId: 商品id
    """

    url = "/mgmt/product/filiale/getFilialeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
