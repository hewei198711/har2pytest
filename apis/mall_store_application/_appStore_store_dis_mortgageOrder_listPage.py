import os

from util.client import client

params = {
    "beginMortgageTime": "",  # 开始押货时间
    "beginTime": "",  # 开始提交时间
    "companyCode": "",  # 所属分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "discountType": 0,  # 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    "endMortgageTime": "",  # 结束押货时间
    "endTime": "",  # 结束提交时间
    "hasLogisticsEvaluation": 0,  # 物流是否已评价 0否 1是
    "hasLogisticsFeedback": 0,  # 物流是否已反馈 0否 1是
    "isLogisticsEvaluationReplied": 0,  # 是否已回复物流评价 0未回复 1已回复
    "isLogisticsFeedbackReplied": 0,  # 是否已回复物流反馈 0未回复 1已回复
    "isShow": 0,  # 是否前端展示 0否 1是
    "isTrafficControl": 0,  # 是否处于交通管制 0否 1是
    "logisticsEvaluation": "",  # 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    "modifyFlag": 0,  # 是否有修改过 0未修改 1已修改
    "needEvaluationId": False,  # TODO: 添加参数说明
    "orderMark": 0,  # 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货 5 1:3转库存押货 6签约购押货 7随心购押货 8换购品押货 9签约购押货3.0
    "orderSn": "",  # 押货单号
    "orderSource": 0,  # 押货单来源 1服务中心押货 2运营后台押货
    "orderStatues": "",  # 押货单状态列表 1待审核 2待支付 3待发货 4部分发货 5已完成 6已取消 7已发货
    "orderStatus": 0,  # 押货单状态 1待审核 2待支付 3待发货 4部分发货 5已完成 6已取消 7已发货
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "payType": 0,  # 支付方式 1保证金 2工行签约代扣 3建行签约代扣 4工行签约代扣+保证金 5建行签约代扣+保证金
    "storeCode": "",  # 服务中心编号
    "storeLeader": False,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_listPage(params=params, headers=headers):
    """
    押货单列表查询
    /appStore/store/dis/mortgageOrder/listPage

    参数说明:
    - beginMortgageTime: 开始押货时间
    - beginTime: 开始提交时间
    - companyCode: 所属分公司编号
    - companyCodeList: 分公司编号列表
    - discountType: 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    - endMortgageTime: 结束押货时间
    - endTime: 结束提交时间
    - hasLogisticsEvaluation: 物流是否已评价 0否 1是
    - hasLogisticsFeedback: 物流是否已反馈 0否 1是
    - isLogisticsEvaluationReplied: 是否已回复物流评价 0未回复 1已回复
    - isLogisticsFeedbackReplied: 是否已回复物流反馈 0未回复 1已回复
    - isShow: 是否前端展示 0否 1是
    - isTrafficControl: 是否处于交通管制 0否 1是
    - logisticsEvaluation: 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    - modifyFlag: 是否有修改过 0未修改 1已修改
    - orderMark: 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货 5 1:3转库存押货 6签约购押货 7随心购押货 8换购品押货 9签约购押货3.0
    - orderSn: 押货单号
    - orderSource: 押货单来源 1服务中心押货 2运营后台押货
    - orderStatues: 押货单状态列表 1待审核 2待支付 3待发货 4部分发货 5已完成 6已取消 7已发货
    - orderStatus: 押货单状态 1待审核 2待支付 3待发货 4部分发货 5已完成 6已取消 7已发货
    - pageNum: 页数
    - pageSize: 页大小
    - payType: 支付方式 1保证金 2工行签约代扣 3建行签约代扣 4工行签约代扣+保证金 5建行签约代扣+保证金
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgageOrder/listPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
