import os

from util.client import client

params = {
    "days": 0,  # days
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_saveRefundThreshold(params=params, headers=headers):
    """
    设置自动退款阈值
    /mgmt/sys/saveRefundThreshold

    参数说明:
    - days: days
    """

    url = "/mgmt/sys/saveRefundThreshold"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
