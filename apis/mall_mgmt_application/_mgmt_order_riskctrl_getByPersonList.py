import os

from util.client import client

data = {
    "auditTimeEnd": "",  # 审批结束时间yyyy-MM-dd
    "auditTimeStart": "",  # 审批开始时间yyyy-MM-dd
    "checkTimeEnd": "",  # 核查结束时间yyyy-MM-dd
    "checkTimeStart": "",  # 核查开始时间yyyy-MM-dd
    "createTimeEnd": "",  # 记录生成结束时间yyyy-MM-dd
    "createTimeStart": "",  # 记录生成开始时间yyyy-MM-dd
    "creatorCard": "",  # 会员卡号
    "creatorName": "",  # 会员姓名
    "creatorPhone": "",  # 会员手机号
    "from": 0,  # TODO: 添加参数说明
    "handleResult": 0,  # 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "warnStatus": 0,  # 当前状态，1：待核查；2：待审批；3：审批通过；4：已驳回
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_getByPersonList(data=data, headers=headers):
    """
    人维度预警报表
    /mgmt/order/riskctrl/getByPersonList

    参数说明:
    - auditTimeEnd: 审批结束时间yyyy-MM-dd
    - auditTimeStart: 审批开始时间yyyy-MM-dd
    - checkTimeEnd: 核查结束时间yyyy-MM-dd
    - checkTimeStart: 核查开始时间yyyy-MM-dd
    - createTimeEnd: 记录生成结束时间yyyy-MM-dd
    - createTimeStart: 记录生成开始时间yyyy-MM-dd
    - creatorCard: 会员卡号
    - creatorName: 会员姓名
    - creatorPhone: 会员手机号
    - handleResult: 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    - pageNum: 页数
    - pageSize: 每页显示数
    - warnStatus: 当前状态，1：待核查；2：待审批；3：审批通过；4：已驳回
    """

    url = "/mgmt/order/riskctrl/getByPersonList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
