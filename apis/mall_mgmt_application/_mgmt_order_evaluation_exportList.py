import os

from util.client import client

params = {
    "branchCode": "",  # 业务分公司编号
    "customerCard": "",  # 顾客卡号
    "deliveryCity": "",  # 收货地址市
    "deliveryMethod": "",  # 交付方式
    "deliveryProvince": "",  # 收货地址省
    "evaluateEndDate": "",  # 评价结束时间
    "evaluateStartDate": "",  # 评价开始时间
    "evaluateStatus": "",  # 评价状态
    "evaluatorType": 0,  # 评价人。0:unknown，1:开单人，2:购货人
    "hasImage": False,  # 是否有图片
    "hasTextContent": False,  # 是否有文字内容
    "isAutoEvaluate": False,  # 是否自动评价
    "isDefault": False,  # 是否默认评价
    "isDisplayOnFrontend": False,  # 是否前端展示
    "isNegativeReview": False,  # 是否差评
    "isQuality": False,  # 是否优质评价
    "isReplied": False,  # 是否回复评价
    "isTop": False,  # 是否评价置顶
    "logisticsRating": 0,  # 物流评价星级数
    "logisticsTags": [],  # 物流评价标签
    "orderNo": "",  # 订单号
    "orderType": "",  # 订单类型
    "pageNum": 0,  # 页码 默认1
    "pageSize": 0,  # 页数 默认10
    "productCode": "",  # 产品编码
    "productRating": 0,  # 产品评价星级数
    "productTags": [],  # 产品评价标签
    "salespersonCard": "",  # 开单人卡号
    "shoppingExperienceRating": 0,  # 购物体验星级数
    "shoppingExperienceTags": [],  # 购物体验标签
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_exportList(params=params, headers=headers):
    """
    导出列表
    /mgmt/order/evaluation/exportList

    参数说明:
    - branchCode: 业务分公司编号
    - customerCard: 顾客卡号
    - deliveryCity: 收货地址市
    - deliveryMethod: 交付方式
    - deliveryProvince: 收货地址省
    - evaluateEndDate: 评价结束时间
    - evaluateStartDate: 评价开始时间
    - evaluateStatus: 评价状态
    - evaluatorType: 评价人。0:unknown，1:开单人，2:购货人
    - hasImage: 是否有图片
    - hasTextContent: 是否有文字内容
    - isAutoEvaluate: 是否自动评价
    - isDefault: 是否默认评价
    - isDisplayOnFrontend: 是否前端展示
    - isNegativeReview: 是否差评
    - isQuality: 是否优质评价
    - isReplied: 是否回复评价
    - isTop: 是否评价置顶
    - logisticsRating: 物流评价星级数
    - logisticsTags: 物流评价标签
    - orderNo: 订单号
    - orderType: 订单类型
    - pageNum: 页码 默认1
    - pageSize: 页数 默认10
    - productCode: 产品编码
    - productRating: 产品评价星级数
    - productTags: 产品评价标签
    - salespersonCard: 开单人卡号
    - shoppingExperienceRating: 购物体验星级数
    - shoppingExperienceTags: 购物体验标签
    """

    url = "/mgmt/order/evaluation/exportList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
