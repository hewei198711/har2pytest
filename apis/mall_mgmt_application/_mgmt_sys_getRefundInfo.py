import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getRefundInfo(headers=headers):
    """
    查询有效退款阈值
    /mgmt/sys/getRefundInfo
    """

    url = "/mgmt/sys/getRefundInfo"
    with client.get(url=url, headers=headers) as r:
        return r
