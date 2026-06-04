import os

from util.client import client

params = {
    "id": "",  # 参数id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_price_getFilialePriceById(params=params, headers=headers):
    """
    查询分公司价格配置参数
    /mgmt/product/price/getFilialePriceById

    参数说明:
    - id: 参数id
    """

    url = "/mgmt/product/price/getFilialePriceById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
