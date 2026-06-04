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


def _mgmt_prmt_rights_exhangProduct_onShelfVersion(data=data, headers=headers):
    """
    兑换产品版本上架
    /mgmt/prmt/rights/exhangProduct/onShelfVersion

    参数说明:
    - exchangeProductId: exchangeProductId
    """

    url = "/mgmt/prmt/rights/exhangProduct/onShelfVersion"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
