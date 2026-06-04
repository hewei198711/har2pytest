import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "id": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editEndTime(data=data, headers=headers):
    """
    修改活动结束时间
    /mgmt/prmt/luckyActivity/editEndTime

    参数说明:
    - endTime: 结束时间
    - id: 活动id
    """

    url = "/mgmt/prmt/luckyActivity/editEndTime"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
