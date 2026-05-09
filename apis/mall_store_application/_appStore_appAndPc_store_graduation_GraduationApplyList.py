import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请时间结束日期 yyyy-MM-dd
    "applyStartTime": "",  # 申请时间开始日期 yyyy-MM-dd
    "auditStatus": 0,  # 审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_GraduationApplyList(data=data, headers=headers):
    """
    结业申请列表--web,app
    /appStore/appAndPc/store/graduation/GraduationApplyList

    参数说明:
    - applyEndTime: 申请时间结束日期 yyyy-MM-dd
    - applyStartTime: 申请时间开始日期 yyyy-MM-dd
    - auditStatus: 审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    """

    url = "/appStore/appAndPc/store/graduation/GraduationApplyList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
