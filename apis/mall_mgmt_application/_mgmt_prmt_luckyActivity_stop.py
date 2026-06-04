import os

from util.client import client

data = {
    "id": 0,  # id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_stop(data=data, headers=headers):
    """
    手动停止抽奖活动
    /mgmt/prmt/luckyActivity/stop

    参数说明:
    - id: id
    - remarks: 备注
    """

    url = "/mgmt/prmt/luckyActivity/stop"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
