import os

from util.client import client

data = {
    "followRemark": "",  # 跟进情况
    "ids": [],  # id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_followOrderNoarrivewarn(data=data, headers=headers):
    """
    跟进订单货物未送达预警
    /mgmt/order/followOrderNoarrivewarn

    参数说明:
    - followRemark: 跟进情况
    - ids: id集合
    """

    url = "/mgmt/order/followOrderNoarrivewarn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
