import os

from util.client import client

data = {
    "cardNo": "",  # 负责人卡号
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号
    "discountLevelList": [],  # 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    "from": 0,  # TODO: 添加参数说明
    "isDifCheck": 0,  # 差额校验是否为零 0->否 1->是
    "isDifference": 0,  # 本期交付差额是否为负 0->否 1->是
    "orderMonth": "",  # 业绩月份
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "realName": "",  # 负责人
    "settlementMonth": "",  # 库存月结月份
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderSettlement(data=data, headers=headers):
    """
    导出交付结算
    /mgmt/order/exportOrderSettlement

    参数说明:
    - cardNo: 负责人卡号
    - companyCode: 分公司编号
    - companyCodes: 分公司编号
    - discountLevelList: 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    - isDifCheck: 差额校验是否为零 0->否 1->是
    - isDifference: 本期交付差额是否为负 0->否 1->是
    - orderMonth: 业绩月份
    - pageNum: 页数
    - pageSize: 每页显示数
    - realName: 负责人
    - settlementMonth: 库存月结月份
    - storeCode: 服务中心编号
    """

    url = "/mgmt/order/exportOrderSettlement"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
