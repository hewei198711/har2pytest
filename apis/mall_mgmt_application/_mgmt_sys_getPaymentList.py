import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getPaymentList(headers=headers):
    """
    findPTAll
    /mgmt/sys/getPaymentList
    """

    url = "/mgmt/sys/getPaymentList"
    with client.get(url=url, headers=headers) as r:
        return r
