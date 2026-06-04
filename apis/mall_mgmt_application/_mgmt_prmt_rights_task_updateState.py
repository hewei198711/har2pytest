import os

from util.client import client

data = {
    "id": 0,  # 主键
    "state": 0,  # 状态:2-启用,3-禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_updateState(data=data, headers=headers):
    """
    更新任务状态（启用、禁用）
    /mgmt/prmt/rights/task/updateState

    参数说明:
    - id: 主键
    - state: 状态:2-启用,3-禁用
    """

    url = "/mgmt/prmt/rights/task/updateState"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
