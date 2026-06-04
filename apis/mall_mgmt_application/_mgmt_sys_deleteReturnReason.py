import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_deleteReturnReason(params=params, headers=headers):
    """
    删除一级或二级原因
    /mgmt/sys/deleteReturnReason

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/deleteReturnReason"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
