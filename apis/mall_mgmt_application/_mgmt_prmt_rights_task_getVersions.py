import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_getVersions(params=params, headers=headers):
    """
    获取历史版本
    /mgmt/prmt/rights/task/getVersions

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/rights/task/getVersions"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
