import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请时间结束日期 yyyy-MM-dd
    "applyStartTime": "",  # 申请时间开始日期 yyyy-MM-dd
    "auditStatus": 0,  # 审核状态 1审核通过 2已驳回 3待审核 4已撤销 5已完成 6完成待受理 7撤销待受理
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_moveApplyList(data=data, headers=headers):
    """
    搬迁申请列表--web,app
    /appStore/webAndApp/store/move/moveApplyList

    参数说明:
    - applyEndTime: 申请时间结束日期 yyyy-MM-dd
    - applyStartTime: 申请时间开始日期 yyyy-MM-dd
    - auditStatus: 审核状态 1审核通过 2已驳回 3待审核 4已撤销 5已完成 6完成待受理 7撤销待受理
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    """

    url = "/appStore/webAndApp/store/move/moveApplyList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
