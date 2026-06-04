import os

from util.client import client

params = {
    "afterMortgageOrderType": 0,  # 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
    "bizMode": 0,  # 经营模式 1->1:3, 2->85
    "companyCode": "",  # 分公司编号
    "evalStatus": 0,  # 评价状态 1待评价 2已评价
    "evalTimeEnd": "",  # 评价时间-结束
    "evalTimeStart": "",  # 评价时间-开始
    "evalWay": 0,  # 评价方式 1主动评价 2超时系统自动评价
    "itemAttitude": 0,  # 评价项-服务态度 1不满意 2一般 3满意 4非常满意
    "itemConvenience": 0,  # 评价项-服务便捷度 1不满意 2一般 3满意 4非常满意
    "itemLogistics": 0,  # 评价项-售后物流评价 1不满意 2一般 3满意 4非常满意
    "itemTimeliness": 0,  # 评价项-服务时效 1不满意 2一般 3满意 4非常满意
    "orderSn": "",  # 售后单编号
    "orderType": 0,  # 售后单类型 1押货退 2押货换 3货损货差
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterMortgage_satisfaction_excel(params=params, headers=headers):
    """
    导出
    /mgmt/afterMortgage/satisfaction/excel

    参数说明:
    - afterMortgageOrderType: 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
    - bizMode: 经营模式 1->1:3, 2->85
    - companyCode: 分公司编号
    - evalStatus: 评价状态 1待评价 2已评价
    - evalTimeEnd: 评价时间-结束
    - evalTimeStart: 评价时间-开始
    - evalWay: 评价方式 1主动评价 2超时系统自动评价
    - itemAttitude: 评价项-服务态度 1不满意 2一般 3满意 4非常满意
    - itemConvenience: 评价项-服务便捷度 1不满意 2一般 3满意 4非常满意
    - itemLogistics: 评价项-售后物流评价 1不满意 2一般 3满意 4非常满意
    - itemTimeliness: 评价项-服务时效 1不满意 2一般 3满意 4非常满意
    - orderSn: 售后单编号
    - orderType: 售后单类型 1押货退 2押货换 3货损货差
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/mgmt/afterMortgage/satisfaction/excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
