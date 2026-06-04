import os

from util.client import client

params = {
    "endTimeEnd": "",  # 任务结束时间止区(yyyy-MM-dd)
    "endTimeStart": "",  # 任务结束时间起区(yyyy-MM-dd)
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTimeEnd": "",  # 任务开始时间止区(yyyy-MM-dd)
    "startTimeStart": "",  # 任务开始时间起区(yyyy-MM-dd)
    "state": 0,  # 状态:0-草稿,1-待审核,2-启用,3-禁用,4-审核不通过,5-已过期
    "taskName": "",  # 任务名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_page(params=params, headers=headers):
    """
    分页查询任务
    /mgmt/prmt/rights/task/page

    参数说明:
    - endTimeEnd: 任务结束时间止区(yyyy-MM-dd)
    - endTimeStart: 任务结束时间起区(yyyy-MM-dd)
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTimeEnd: 任务开始时间止区(yyyy-MM-dd)
    - startTimeStart: 任务开始时间起区(yyyy-MM-dd)
    - state: 状态:0-草稿,1-待审核,2-启用,3-禁用,4-审核不通过,5-已过期
    - taskName: 任务名称
    """

    url = "/mgmt/prmt/rights/task/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
