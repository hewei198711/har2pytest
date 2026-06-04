import os

from util.client import client

params = {
    "id": "",  # 参数id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_price_deleteFilialePrice(params=params, headers=headers):
    """
    删除分公司价格参数配置
    /mgmt/product/price/deleteFilialePrice

    参数说明:
    - id: 参数id
    """

    url = "/mgmt/product/price/deleteFilialePrice"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
