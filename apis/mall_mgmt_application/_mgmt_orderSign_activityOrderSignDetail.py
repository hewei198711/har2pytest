import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_activityOrderSignDetail(params=params, headers=headers):
    """
    活动中心 > 签约购活动管理 > 签约购活动详情 > 签约情况列表 > 详情
    /mgmt/orderSign/activityOrderSignDetail

    参数说明:
    - signNo: signNo
    """

    url = "/mgmt/orderSign/activityOrderSignDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
