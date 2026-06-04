import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getLogisticsList(headers=headers):
    """
    展示所有物流类型页面
    /mgmt/sys/getLogisticsList
    """

    url = "/mgmt/sys/getLogisticsList"
    with client.get(url=url, headers=headers) as r:
        return r
