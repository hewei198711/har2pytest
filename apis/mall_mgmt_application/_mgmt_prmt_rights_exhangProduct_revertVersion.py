import os
from urllib.parse import urlencode

from util.client import client

data = {
    "verId": "",  # verId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_rights_exhangProduct_revertVersion(data=data, headers=headers):
    """
    兑换产品版本撤回
    /mgmt/prmt/rights/exhangProduct/revertVersion

    参数说明:
    - verId: verId
    """

    url = "/mgmt/prmt/rights/exhangProduct/revertVersion"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
