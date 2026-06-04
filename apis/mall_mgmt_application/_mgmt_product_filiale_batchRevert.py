import os

from util.client import client

params = {
    "productIds": "",  # 商品id数组
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_batchRevert(params=params, headers=headers):
    """
    分公司价格信息批量撤回
    /mgmt/product/filiale/batchRevert

    参数说明:
    - productIds: 商品id数组
    """

    url = "/mgmt/product/filiale/batchRevert"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
