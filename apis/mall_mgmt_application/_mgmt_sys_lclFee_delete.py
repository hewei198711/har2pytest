import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFee_delete(params=params, headers=headers):
    """
    删除拼箱费模板
    /mgmt/sys/lclFee/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/lclFee/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
