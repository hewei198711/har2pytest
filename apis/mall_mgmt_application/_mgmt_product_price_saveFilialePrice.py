import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_price_saveFilialePrice(headers=headers):
    """
    保存分公司价格配置列表
    /mgmt/product/price/saveFilialePrice
    """

    url = "/mgmt/product/price/saveFilialePrice"
    with client.post(url=url, headers=headers) as r:
        return r
