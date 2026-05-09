import os

from util.client import client

params = {
    "beginTime": "",  # 开始押货时间
    "customFlag": 0,  # 是否为定制品押货单 0否 1是
    "endTime": "",  # 结束押货时间
    "hasLogisticsEvaluation": 0,  # 物流是否已评价 0否 1是
    "hasLogisticsFeedback": 0,  # 物流是否已反馈 0否 1是
    "isLogisticsEvaluationReplied": 0,  # 是否已回复物流评价 0未回复 1已回复
    "isLogisticsFeedbackReplied": 0,  # 是否已回复物流反馈 0未回复 1已回复
    "logisticsEvaluation": "",  # 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    "orderMark": 0,  # 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    "orderSn": "",  # 押货单号
    "orderSource": 0,  # 押货单来源 1服务中心押货 2运营后台押货
    "orderStatus": 0,  # 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消（审核不通过）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_page(params=params, headers=headers):
    """
    押货单列表（分页）
    /appStore/purchaseOrder/page

    参数说明:
    - beginTime: 开始押货时间
    - customFlag: 是否为定制品押货单 0否 1是
    - endTime: 结束押货时间
    - hasLogisticsEvaluation: 物流是否已评价 0否 1是
    - hasLogisticsFeedback: 物流是否已反馈 0否 1是
    - isLogisticsEvaluationReplied: 是否已回复物流评价 0未回复 1已回复
    - isLogisticsFeedbackReplied: 是否已回复物流反馈 0未回复 1已回复
    - logisticsEvaluation: 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    - orderMark: 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    - orderSn: 押货单号
    - orderSource: 押货单来源 1服务中心押货 2运营后台押货
    - orderStatus: 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消（审核不通过）
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/purchaseOrder/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
