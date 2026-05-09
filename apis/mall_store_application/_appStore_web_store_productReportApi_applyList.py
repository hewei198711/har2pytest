import os

from util.client import client

params = {
    "applyEndTime": "",  # 申请时间结束日期 yyyy-MM-dd
    "applyReason": "",  # 申请原因
    "applyStartTime": "",  # 申请时间开始日期 yyyy-MM-dd
    "codeOrName": "",  # 服务中心编号或名称
    "companyCode": "",  # 所属分公司编号
    "companyCodes": [],  # 所属分公司编号列表
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "status": 0,  # 状态 0全部 1审核通过 2已驳回 3待审核
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_productReportApi_applyList(params=params, headers=headers):
    """
    成品报告申请列表
    /appStore/web/store/productReportApi/applyList

    参数说明:
    - applyEndTime: 申请时间结束日期 yyyy-MM-dd
    - applyReason: 申请原因
    - applyStartTime: 申请时间开始日期 yyyy-MM-dd
    - codeOrName: 服务中心编号或名称
    - companyCode: 所属分公司编号
    - companyCodes: 所属分公司编号列表
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - status: 状态 0全部 1审核通过 2已驳回 3待审核
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/store/productReportApi/applyList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
