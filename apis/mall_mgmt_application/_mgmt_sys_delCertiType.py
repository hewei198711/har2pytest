import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_delCertiType(params=params, headers=headers):
    """
    删除类型
    /mgmt/sys/delCertiType

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/delCertiType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
