import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getComInfo(params=params, headers=headers):
    """
    显示company的详情
    /mgmt/sys/getComInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/getComInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
