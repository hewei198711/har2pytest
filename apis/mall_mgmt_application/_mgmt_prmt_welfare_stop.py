import os

from util.client import client

params = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_stop(params=params, headers=headers):
    """
    手动停止活动
    /mgmt/prmt/welfare/stop

    参数说明:
    - id: 活动id
    """

    url = "/mgmt/prmt/welfare/stop"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
