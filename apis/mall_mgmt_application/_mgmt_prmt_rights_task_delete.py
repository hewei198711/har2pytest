import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_delete(data=data, headers=headers):
    """
    删除任务
    /mgmt/prmt/rights/task/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/rights/task/delete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
