import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getMonCfg(headers=headers):
    """
    获取月结的日期
    /mgmt/sys/getMonCfg
    """

    url = "/mgmt/sys/getMonCfg"
    with client.get(url=url, headers=headers) as r:
        return r
