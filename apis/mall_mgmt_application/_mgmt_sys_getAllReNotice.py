import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getAllReNotice(headers=headers):
    """
    获取退货须知集合
    /mgmt/sys/getAllReNotice
    """

    url = "/mgmt/sys/getAllReNotice"
    with client.get(url=url, headers=headers) as r:
        return r
