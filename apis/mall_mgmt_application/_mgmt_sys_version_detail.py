import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_version_detail(params=params, headers=headers):
    """
    根据id查看版本详情
    /mgmt/sys/version/detail

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/version/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
