import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_currentSettings(headers=headers):
    """
    获取评价时限设置
    /mgmt/order/evaluation/currentSettings
    """

    url = "/mgmt/order/evaluation/currentSettings"
    with client.get(url=url, headers=headers) as r:
        return r
