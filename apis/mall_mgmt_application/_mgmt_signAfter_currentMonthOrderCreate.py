import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_signAfter_currentMonthOrderCreate(params=params, headers=headers):
    """
    签约购当月子订单是否已生成
    /mgmt/signAfter/currentMonthOrderCreate

    参数说明:
    - signNo: signNo
    """

    url = "/mgmt/signAfter/currentMonthOrderCreate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
