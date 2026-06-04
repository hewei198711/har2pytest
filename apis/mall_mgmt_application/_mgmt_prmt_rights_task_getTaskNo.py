import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_getTaskNo(headers=headers):
    """
    新增任务时获取任务编号
    /mgmt/prmt/rights/task/getTaskNo
    """

    url = "/mgmt/prmt/rights/task/getTaskNo"
    with client.get(url=url, headers=headers) as r:
        return r
