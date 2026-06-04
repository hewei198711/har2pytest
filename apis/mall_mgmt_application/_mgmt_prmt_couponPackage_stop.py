import os

from util.client import client

params = {
    "id": "",  # 活动id
    "stopReason": "",  # stopReason
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_stop(params=params, headers=headers):
    """
    手动停止任务
    /mgmt/prmt/couponPackage/stop

    参数说明:
    - id: 活动id
    - stopReason: stopReason
    """

    url = "/mgmt/prmt/couponPackage/stop"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
