import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_getOrderSignLog(params=params, headers=headers):
    """
    签约售后列表-签约单操作记录
    /mgmt/orderSign/getOrderSignLog

    参数说明:
    - signNo: signNo
    """

    url = "/mgmt/orderSign/getOrderSignLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
