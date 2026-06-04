import os
from urllib.parse import urlencode

from util.client import client

data = {
    "exchangeProductId": "",  # exchangeProductId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_rights_exhangProduct_offShelfVersion(data=data, headers=headers):
    """
    兑换产品版本下架
    /mgmt/prmt/rights/exhangProduct/offShelfVersion

    参数说明:
    - exchangeProductId: exchangeProductId
    """

    url = "/mgmt/prmt/rights/exhangProduct/offShelfVersion"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
