import os
from urllib.parse import urlencode

from util.client import client

data = {
    "verIds": [],  # verIds
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_rights_exhangProduct_batchDel(data=data, headers=headers):
    """
    兑换产品版本删除
    /mgmt/prmt/rights/exhangProduct/batchDel

    参数说明:
    - verIds: verIds
    """

    url = "/mgmt/prmt/rights/exhangProduct/batchDel"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
