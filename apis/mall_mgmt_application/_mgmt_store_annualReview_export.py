import os

from util.client import client

params = {
    "companyCode": "",  # 分公司code
    "companyCodes": [],  # 分公司编码列表
    "endApplyTime": "",  # 申请时间(结束)  yyyy-MM-dd 格式
    "endVerifyTime": "",  # 审核时间(结束)  yyyy-MM-dd 格式
    "fileName": "",  # 文件名称
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页数
    "reviewModelType": 0,  # 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    "startApplyTime": "",  # 申请时间(开始)  yyyy-MM-dd 格式
    "startVerifyTime": "",  # 审核时间(开始)  yyyy-MM-dd 格式
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 0 带审核,1 审核通过,3 已驳回
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_export(params=params, headers=headers):
    """
    年审审批列表导出
    /mgmt/store/annualReview/export

    参数说明:
    - companyCode: 分公司code
    - companyCodes: 分公司编码列表
    - endApplyTime: 申请时间(结束)  yyyy-MM-dd 格式
    - endVerifyTime: 审核时间(结束)  yyyy-MM-dd 格式
    - fileName: 文件名称
    - pageNum: 页码
    - pageSize: 页数
    - reviewModelType: 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    - startApplyTime: 申请时间(开始)  yyyy-MM-dd 格式
    - startVerifyTime: 审核时间(开始)  yyyy-MM-dd 格式
    - storeCode: 服务中心编号
    - verifyStatus: 0 带审核,1 审核通过,3 已驳回
    """

    url = "/mgmt/store/annualReview/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
