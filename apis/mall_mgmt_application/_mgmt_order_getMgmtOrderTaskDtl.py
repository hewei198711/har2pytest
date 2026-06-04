import os

from util.client import client

params = {
    "taskId": 0,  # 任务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getMgmtOrderTaskDtl(params=params, headers=headers):
    """
    分级押货模式查看转分记录失败记录
    /mgmt/order/getMgmtOrderTaskDtl

    参数说明:
    - taskId: 任务id
    """

    url = "/mgmt/order/getMgmtOrderTaskDtl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
