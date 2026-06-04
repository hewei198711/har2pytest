import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getProductList(params=params, headers=headers):
    """
    根据关键字模糊查询商品信息
    /mgmt/order/factory/getProductList

    参数说明:
    - keyword: keyword
    """

    url = "/mgmt/order/factory/getProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
