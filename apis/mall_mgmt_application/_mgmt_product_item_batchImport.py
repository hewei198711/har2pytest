import os
from urllib.parse import urlencode

from util.client import client

data = {
    "url": "",  # 上传到oss后返回的excel地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_item_batchImport(data=data, headers=headers):
    """
    批量上传excel
    /mgmt/product/item/batchImport

    参数说明:
    - url: 上传到oss后返回的excel地址
    """

    url = "/mgmt/product/item/batchImport"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
