import os

from util.client import client

params = {
    "year": "",  # 年
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getMonCfgLog(params=params, headers=headers):
    """
    展示月结历史记录
    /mgmt/sys/getMonCfgLog

    参数说明:
    - year: 年
    """

    url = "/mgmt/sys/getMonCfgLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
