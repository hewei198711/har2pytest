import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getFaultReason(headers=headers):
    """
    故障原因列表
    /mgmt/sys/getFaultReason
    """

    url = "/mgmt/sys/getFaultReason"
    with client.get(url=url, headers=headers) as r:
        return r
