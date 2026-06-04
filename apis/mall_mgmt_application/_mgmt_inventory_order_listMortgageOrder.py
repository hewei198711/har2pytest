import os

from util.client import client

params = {
    "beginTime": "",  # 开始押货时间
    "companyCode": "",  # 所属分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "customFlag": 0,  # 是否有为定制品押货单 0不是 1是
    "editFlag": 0,  # 是否有修改过 0未修改 1已修改
    "endTime": "",  # 结束押货时间
    "isLogisticsEvaluationReplied": 0,  # 是否已回复物流评价 0未回复 1已回复
    "isLogisticsFeedbackReplied": 0,  # 是否已回复物流反馈 0未回复 1已回复
    "isTrafficControl": 0,  # 是否交通管制 0否 1是
    "logisticsEvaluation": "",  # 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    "logisticsFeedback": "",  # 物流反馈(逗号隔开) 0未反馈 1延迟到货 2货损 3货差 4服务态度差
    "orderMark": 0,  # 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    "orderSn": "",  # 押货单号
    "orderSource": 0,  # 押货单来源
    "orderStatus": 0,  # 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消 6已发货
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_listMortgageOrder(params=params, headers=headers):
    """
    运营后台押货单列表查询
    /mgmt/inventory/order/listMortgageOrder

    参数说明:
    - beginTime: 开始押货时间
    - companyCode: 所属分公司编号
    - companyCodeList: 分公司编号列表
    - customFlag: 是否有为定制品押货单 0不是 1是
    - editFlag: 是否有修改过 0未修改 1已修改
    - endTime: 结束押货时间
    - isLogisticsEvaluationReplied: 是否已回复物流评价 0未回复 1已回复
    - isLogisticsFeedbackReplied: 是否已回复物流反馈 0未回复 1已回复
    - isTrafficControl: 是否交通管制 0否 1是
    - logisticsEvaluation: 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    - logisticsFeedback: 物流反馈(逗号隔开) 0未反馈 1延迟到货 2货损 3货差 4服务态度差
    - orderMark: 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    - orderSn: 押货单号
    - orderSource: 押货单来源
    - orderStatus: 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消 6已发货
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/order/listMortgageOrder"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
