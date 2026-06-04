import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_welfare_importProduct(headers=headers):
    """
    解析导入商品
    /mgmt/prmt/welfare/importProduct
    """

    url = "/mgmt/prmt/welfare/importProduct"
    with client.post(url=url, headers=headers) as r:
        return r
