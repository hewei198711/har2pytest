import os
from urllib.parse import urlencode

from util.client import client

data = {
    "distId": "",  # 分配量id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_quota_delProduct(data=data, headers=headers):
    """
    删除产品
    /mgmt/product/quota/delProduct

    参数说明:
    - distId: 分配量id
    """

    url = "/mgmt/product/quota/delProduct"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
