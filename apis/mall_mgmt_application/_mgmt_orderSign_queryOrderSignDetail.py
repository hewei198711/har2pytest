import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_queryOrderSignDetail(params=params, headers=headers):
    """
    报表中心> 签约管理报表 > 详情
    /mgmt/orderSign/queryOrderSignDetail

    参数说明:
    - signNo: signNo
    """

    url = "/mgmt/orderSign/queryOrderSignDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
