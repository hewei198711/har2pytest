import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFeeCeiling_delete(params=params, headers=headers):
    """
    删除拼箱费上限
    /mgmt/sys/lclFeeCeiling/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/lclFeeCeiling/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
