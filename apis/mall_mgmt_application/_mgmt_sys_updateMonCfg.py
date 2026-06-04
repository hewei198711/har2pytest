import os

from util.client import client

params = {
    "newDay": "",  # 设置的日期 1-28
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateMonCfg(params=params, headers=headers):
    """
    设置月结日期
    /mgmt/sys/updateMonCfg

    参数说明:
    - newDay: 设置的日期 1-28
    """

    url = "/mgmt/sys/updateMonCfg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
