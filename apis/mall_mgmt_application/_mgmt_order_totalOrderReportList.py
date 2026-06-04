import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号
    "companyName": "",  # 分公司名称
    "discountLevelList": [],  # 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    "expressType": 0,  # 交付方式 1->服务中心自提 2->公司交付
    "orderMonths": [],  # 业绩月份yyyyMM
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "stockType": 0,  # 经营模式 1->1:3押货 2->85折押货
    "storeCode": "",  # 服务中心编号
    "storeLeader": "",  # 负责人
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_totalOrderReportList(data=data, headers=headers):
    """
    订单销售月报合计
    /mgmt/order/totalOrderReportList

    参数说明:
    - companyCode: 分公司编号
    - companyCodes: 分公司编号
    - companyName: 分公司名称
    - discountLevelList: 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    - expressType: 交付方式 1->服务中心自提 2->公司交付
    - orderMonths: 业绩月份yyyyMM
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 每页显示数
    - stockType: 经营模式 1->1:3押货 2->85折押货
    - storeCode: 服务中心编号
    - storeLeader: 负责人
    - storeName: 服务中心名称
    """

    url = "/mgmt/order/totalOrderReportList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
