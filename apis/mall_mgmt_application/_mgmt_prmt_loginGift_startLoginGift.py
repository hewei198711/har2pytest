import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "id": 0,  # 活动id
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_startLoginGift(data=data, headers=headers):
    """
    停止、已结束状态下 启动任务
    /mgmt/prmt/loginGift/startLoginGift

    参数说明:
    - endTime: 结束时间
    - id: 活动id
    - startTime: 开始时间
    """

    url = "/mgmt/prmt/loginGift/startLoginGift"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
