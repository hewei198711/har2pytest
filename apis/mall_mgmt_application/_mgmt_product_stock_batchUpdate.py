import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_stock_batchUpdate(headers=headers):
    """
    批量库存配置
    /mgmt/product/stock/batchUpdate
    """

    url = "/mgmt/product/stock/batchUpdate"
    with client.post(url=url, headers=headers) as r:
        return r
