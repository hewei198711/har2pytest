import os

from util.client import client

data = {
    "auditTimeEnd": "",  # 审批结束时间yyyy-MM-dd
    "auditTimeStart": "",  # 审批开始时间yyyy-MM-dd
    "checkTimeEnd": "",  # 核查结束时间yyyy-MM-dd
    "checkTimeStart": "",  # 核查开始时间yyyy-MM-dd
    "companyCode": "",  # 业务分公司
    "createTimeEnd": "",  # 记录生成结束时间yyyy-MM-dd
    "createTimeStart": "",  # 记录生成开始时间yyyy-MM-dd
    "creatorCard": "",  # 开单人卡号
    "creatorName": "",  # 开单人姓名
    "creatorPhone": "",  # 开单人手机号
    "customerCard": "",  # 购货人卡号
    "customerName": "",  # 购货人姓名
    "customerPhone": "",  # 购货人手机号
    "financeCompanyCode": "",  # 财务分公司
    "from": 0,  # TODO: 添加参数说明
    "handleResult": 0,  # 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    "orderNo": "",  # 订单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "storeCode": "",  # 购货人归属店号
    "warnStatus": 0,  # 当前状态，1：待核查；2：待审批；3：审批通过；4：已驳回
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_exportByOrderList(data=data, headers=headers):
    """
    导出订单维度预警报表
    /mgmt/order/riskctrl/exportByOrderList

    参数说明:
    - auditTimeEnd: 审批结束时间yyyy-MM-dd
    - auditTimeStart: 审批开始时间yyyy-MM-dd
    - checkTimeEnd: 核查结束时间yyyy-MM-dd
    - checkTimeStart: 核查开始时间yyyy-MM-dd
    - companyCode: 业务分公司
    - createTimeEnd: 记录生成结束时间yyyy-MM-dd
    - createTimeStart: 记录生成开始时间yyyy-MM-dd
    - creatorCard: 开单人卡号
    - creatorName: 开单人姓名
    - creatorPhone: 开单人手机号
    - customerCard: 购货人卡号
    - customerName: 购货人姓名
    - customerPhone: 购货人手机号
    - financeCompanyCode: 财务分公司
    - handleResult: 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    - orderNo: 订单号
    - pageNum: 页数
    - pageSize: 每页显示数
    - storeCode: 购货人归属店号
    - warnStatus: 当前状态，1：待核查；2：待审批；3：审批通过；4：已驳回
    """

    url = "/mgmt/order/riskctrl/exportByOrderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
