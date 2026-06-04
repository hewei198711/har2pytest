import os

from util.client import client

params = {
    "id": "",  # 主键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_delFittingById(params=params, headers=headers):
    """
    通过主键删除配件
    /mgmt/sys/delFittingById

    参数说明:
    - id: 主键
    """

    url = "/mgmt/sys/delFittingById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
