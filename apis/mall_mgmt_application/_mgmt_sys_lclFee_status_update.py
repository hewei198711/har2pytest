import os

from util.client import client

params = {
    "id": 0,  # id
    "status": 0,  # status
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFee_status_update(params=params, headers=headers):
    """
    修改拼箱费模板状态
    /mgmt/sys/lclFee/status/update

    参数说明:
    - id: id
    - status: status
    """

    url = "/mgmt/sys/lclFee/status/update"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
