import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作记录
    "id": "",  # 任务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_get(params=params, headers=headers):
    """
    获取任务信息（详情或编辑回显）
    /mgmt/prmt/rights/task/get

    参数说明:
    - getLogs: 是否获取操作记录
    - id: 任务id
    """

    url = "/mgmt/prmt/rights/task/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
