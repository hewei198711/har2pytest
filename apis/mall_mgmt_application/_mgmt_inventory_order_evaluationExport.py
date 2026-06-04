import os

from util.client import client

params = {
    "bizMode": 0,  # 业务类型 1->1:3押货单 2->分级押货单
    "companyCode": "",  # 分公司编号
    "companyCodeList": [],  # TODO: 添加参数说明
    "isEstablished": 0,  # 是否客诉成立 0否 1是
    "isLogisticsEvaluationReplied": 0,  # 是否已回复评价 0否 1是
    "isLogisticsFeedbackReplied": 0,  # 是否已回复反馈 0否 1是
    "isNeedPics": False,  # 是否需要返回物流图片数据
    "logisticsEvaluationEndTime": "",  # 提交评价结束时间
    "logisticsEvaluationStartTime": "",  # 提交评价开始时间
    "logisticsEvaluations": "",  # 物流评价 0未评价 1非常好 2好 3差 4一般 5非常差
    "logisticsFeedbackEndTime": "",  # 提交反馈结束时间
    "logisticsFeedbackStartTime": "",  # 提交反馈开始时间
    "logisticsFeedbacks": "",  # 反馈 1送货不及时 2产品破损 3少货 4物流服务态度不好 5发货不及时 6不送货上门 7快递包装简陋 8快递包装破损 9其他 10不配合开箱验货 11分批送货
    "mortgageEndTime": "",  # 押货结束时间
    "mortgageStartTime": "",  # 押货开始时间
    "orderSn": "",  # 押货单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "selectNew": False,  # TODO: 添加参数说明
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_evaluationExport(params=params, headers=headers):
    """
    押货单物流评价导出Excel
    /mgmt/inventory/order/evaluationExport

    参数说明:
    - bizMode: 业务类型 1->1:3押货单 2->分级押货单
    - companyCode: 分公司编号
    - isEstablished: 是否客诉成立 0否 1是
    - isLogisticsEvaluationReplied: 是否已回复评价 0否 1是
    - isLogisticsFeedbackReplied: 是否已回复反馈 0否 1是
    - isNeedPics: 是否需要返回物流图片数据
    - logisticsEvaluationEndTime: 提交评价结束时间
    - logisticsEvaluationStartTime: 提交评价开始时间
    - logisticsEvaluations: 物流评价 0未评价 1非常好 2好 3差 4一般 5非常差
    - logisticsFeedbackEndTime: 提交反馈结束时间
    - logisticsFeedbackStartTime: 提交反馈开始时间
    - logisticsFeedbacks: 反馈 1送货不及时 2产品破损 3少货 4物流服务态度不好 5发货不及时 6不送货上门 7快递包装简陋 8快递包装破损 9其他 10不配合开箱验货 11分批送货
    - mortgageEndTime: 押货结束时间
    - mortgageStartTime: 押货开始时间
    - orderSn: 押货单号
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/order/evaluationExport"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
