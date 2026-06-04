import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getTaxRate(headers=headers):
    """
    查询所有税率信息
    /mgmt/sys/getTaxRate
    """

    url = "/mgmt/sys/getTaxRate"
    with client.get(url=url, headers=headers) as r:
        return r
