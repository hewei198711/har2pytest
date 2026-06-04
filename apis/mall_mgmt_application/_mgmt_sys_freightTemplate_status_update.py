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


def _mgmt_sys_freightTemplate_status_update(params=params, headers=headers):
    """
    修改运费模板的状态
    /mgmt/sys/freightTemplate/status/update

    参数说明:
    - id: id
    - status: status
    """

    url = "/mgmt/sys/freightTemplate/status/update"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
