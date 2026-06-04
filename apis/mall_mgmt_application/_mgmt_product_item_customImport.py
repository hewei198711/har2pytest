import os

from util.client import client

params = {
    "url": "",  # 上传到oss后返回的excel地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_customImport(params=params, headers=headers):
    """
    批量上传二级产品excel
    /mgmt/product/item/customImport

    参数说明:
    - url: 上传到oss后返回的excel地址
    """

    url = "/mgmt/product/item/customImport"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
