import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getRemittanceList(headers=headers):
    """
    汇款类型展示页
    /mgmt/sys/getRemittanceList
    """

    url = "/mgmt/sys/getRemittanceList"
    with client.get(url=url, headers=headers) as r:
        return r
