import os

from util.client import client

data = {
    "applyId": 0,  # 成品报告申请id
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "producedAddress": 0,  # 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    "producedEndDate": "",  # 生产日期结束日期 yyyy-MM-dd
    "producedStartDate": "",  # 生产日期开始日期(店铺运营的生产日期) yyyy-MM-dd
    "productCode": "",  # 成品代码
    "productName": "",  # 成品名称
    "productNumber": "",  # 批号
    "reportType": 0,  # 报告类型:1自检;2外检
    "sign": 0,  # 标识 0:后台 1:LIMS
    "status": 0,  # 状态 0 禁用 1 启用
    "uploadEndTime": "",  # 上传时间截止时间 yyyy-MM-dd
    "uploadStartTime": "",  # 上传时间开始时间 yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_pageList(data=data, headers=headers):
    """
    成品报告管理列表
    /mgmt/store/productReportManage/pageList

    参数说明:
    - applyId: 成品报告申请id
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - producedAddress: 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    - producedEndDate: 生产日期结束日期 yyyy-MM-dd
    - producedStartDate: 生产日期开始日期(店铺运营的生产日期) yyyy-MM-dd
    - productCode: 成品代码
    - productName: 成品名称
    - productNumber: 批号
    - reportType: 报告类型:1自检;2外检
    - sign: 标识 0:后台 1:LIMS
    - status: 状态 0 禁用 1 启用
    - uploadEndTime: 上传时间截止时间 yyyy-MM-dd
    - uploadStartTime: 上传时间开始时间 yyyy-MM-dd
    """

    url = "/mgmt/store/productReportManage/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
