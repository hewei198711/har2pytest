import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_price_getFilialePriceList(headers=headers):
    """
    分公司价格参数列表
    /mgmt/product/price/getFilialePriceList
    """

    url = "/mgmt/product/price/getFilialePriceList"
    with client.get(url=url, headers=headers) as r:
        return r
