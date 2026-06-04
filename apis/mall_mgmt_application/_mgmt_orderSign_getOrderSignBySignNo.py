import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_getOrderSignBySignNo(params=params, headers=headers):
    """
    根据签约单号查询签约单信息
    /mgmt/orderSign/getOrderSignBySignNo

    参数说明:
    - signNo: signNo
    """

    url = "/mgmt/orderSign/getOrderSignBySignNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
