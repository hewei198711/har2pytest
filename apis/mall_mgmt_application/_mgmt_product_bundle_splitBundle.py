import os
from urllib.parse import urlencode

from util.client import client

data = {
    "splitId": "",  # 拆分id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_bundle_splitBundle(data=data, headers=headers):
    """
    拆分单个套装
    /mgmt/product/bundle/splitBundle

    参数说明:
    - splitId: 拆分id
    """

    url = "/mgmt/product/bundle/splitBundle"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
