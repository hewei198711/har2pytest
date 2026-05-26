import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_sys_getCarriList(headers=headers):
    """
    查询所有的运费模板
    /mgmt/sys/getCarriList
    """

    url = "/mgmt/sys/getCarriList"
    with client.get(url=url, headers=headers) as r:
        return r
