import os

from util.client import client

data = {
    "date": "",  # 生产日期(yyyy-MM-dd)
    "producedAddress": 0,  # 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    "productCode": "",  # 产品代码
    "productName": "",  # 成品名称
    "productNumber": "",  # 批号
    "reportType": 0,  # 报告类型:1自检;2外检
    "status": 0,  # 状态 0 禁用 1 启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_getReportIds(data=data, headers=headers):
    """
    根据条件查询报告,返回id的集合
    /mgmt/store/productReportManage/getReportIds

    参数说明:
    - date: 生产日期(yyyy-MM-dd)
    - producedAddress: 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    - productCode: 产品代码
    - productName: 成品名称
    - productNumber: 批号
    - reportType: 报告类型:1自检;2外检
    - status: 状态 0 禁用 1 启用
    """

    url = "/mgmt/store/productReportManage/getReportIds"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
