import os

from util.client import client

data = {
    "offReason": "",  # 下架原因
    "shareTaskId": 0,  # 分享任务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_stopTask(data=data, headers=headers):
    """
    下架
    /mgmt/prmt/share/stopTask

    参数说明:
    - offReason: 下架原因
    - shareTaskId: 分享任务id
    """

    url = "/mgmt/prmt/share/stopTask"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
