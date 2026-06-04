import os

from util.client import client

params = {
    "companyCodes": [],  # 分公司编号列表
    "companyName": "",  # 分公司编号
    "endApproveTime": "",  # 审批结束时间，例如：2025-09-30
    "endCompleteMoveTime": "",  # 完成搬迁结束时间
    "endTime": "",  # 申请的结束时间
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "startApproveTime": "",  # 审批起始时间，例如：2025-09-01
    "startCompleteMoveTime": "",  # 完成搬迁起始时间
    "startTime": "",  # 申请的起始时间
    "storeCodeOrName": "",  # 店铺编号或名称
    "tabType": "",  # tab类型：ALL 全部，OVERDUE 逾期搬迁
    "verifyStatus": "",  # 审核状态 1审核通过 2已驳回 3待审核 4已撤销 5已完成 6完成待受理 7撤销待受理
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_move_exportStoreMoveInfoList(params=params, headers=headers):
    """
    批量导出搬迁申请记录
    /mgmt/store/move/exportStoreMoveInfoList

    参数说明:
    - companyCodes: 分公司编号列表
    - companyName: 分公司编号
    - endApproveTime: 审批结束时间，例如：2025-09-30
    - endCompleteMoveTime: 完成搬迁结束时间
    - endTime: 申请的结束时间
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - startApproveTime: 审批起始时间，例如：2025-09-01
    - startCompleteMoveTime: 完成搬迁起始时间
    - startTime: 申请的起始时间
    - storeCodeOrName: 店铺编号或名称
    - tabType: tab类型：ALL 全部，OVERDUE 逾期搬迁
    - verifyStatus: 审核状态 1审核通过 2已驳回 3待审核 4已撤销 5已完成 6完成待受理 7撤销待受理
    """

    url = "/mgmt/store/move/exportStoreMoveInfoList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
