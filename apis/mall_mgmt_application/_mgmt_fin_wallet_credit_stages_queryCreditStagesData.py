import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号
    "creditDeductedFlag": 0,  # 是否当月暂不扣除 1：扣除,0：不做扣除
    "creditExeDate": "",  # 执行日期
    "creditExecutedPeriods": 0,  # 已执行期数
    "creditSetPeriods": 0,  # 设置期数
    "eachReduceAmt": 0.0,  # 每期执行金额
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "repaymentAgreementSigned": 0,  # 是否已签署还款协议 0 、否 1、是
    "stageStatus": "",  # 状态：0:待生效，1：进行中，2：已完成 3：已取消
    "storeCode": "",  # 服务中心编号
    "submitEndTime": "",  # 提交结束日期
    "submitStartTime": "",  # 提交开始日期
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_queryCreditStagesData(data=data, headers=headers):
    """
    信用分期管理搜索（查询）
    /mgmt/fin/wallet/credit/stages/queryCreditStagesData

    参数说明:
    - cardNo: 会员卡号
    - companyCode: 分公司编号
    - creditDeductedFlag: 是否当月暂不扣除 1：扣除,0：不做扣除
    - creditExeDate: 执行日期
    - creditExecutedPeriods: 已执行期数
    - creditSetPeriods: 设置期数
    - eachReduceAmt: 每期执行金额
    - pageNum: 页数
    - pageSize: 每页显示数
    - repaymentAgreementSigned: 是否已签署还款协议 0 、否 1、是
    - stageStatus: 状态：0:待生效，1：进行中，2：已完成 3：已取消
    - storeCode: 服务中心编号
    - submitEndTime: 提交结束日期
    - submitStartTime: 提交开始日期
    """

    url = "/mgmt/fin/wallet/credit/stages/queryCreditStagesData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
