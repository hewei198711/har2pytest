import os

from util.client import client

params = {
    "id": 0,  # id
    "status": 0,  # 状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_alterCarriPermission(params=params, headers=headers):
    """
    更改运费模板的权限
    /mgmt/sys/alterCarriPermission

    参数说明:
    - id: id
    - status: 状态
    """

    url = "/mgmt/sys/alterCarriPermission"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
