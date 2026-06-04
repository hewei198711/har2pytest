import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getOrderConfig(params=params, headers=headers):
    """
    通过主键获取SysOrderConfig
    /mgmt/sys/getOrderConfig

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/getOrderConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
