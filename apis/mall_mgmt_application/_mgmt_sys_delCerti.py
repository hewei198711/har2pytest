import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_delCerti(params=params, headers=headers):
    """
    删除证件
    /mgmt/sys/delCerti

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/delCerti"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
