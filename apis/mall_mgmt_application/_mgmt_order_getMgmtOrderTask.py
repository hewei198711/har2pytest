import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getMgmtOrderTask(headers=headers):
    """
    分级押货模式查看转分记录
    /mgmt/order/getMgmtOrderTask
    """

    url = "/mgmt/order/getMgmtOrderTask"
    with client.get(url=url, headers=headers) as r:
        return r
