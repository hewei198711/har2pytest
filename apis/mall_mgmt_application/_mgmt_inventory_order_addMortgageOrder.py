import os

from util.client import client

data = {
    "invtMortgageOrderProductVOList": [
        {
            "createTime": "",
            "del": 0,
            "id": 0,
            "isGift": 0,
            "orderId": 0,
            "orderSn": "",
            "productBoxNum": 0,
            "productCode": "",
            "productDeliveredNum": 0,
            "productId": 0,
            "productMortgagePrice": 0.0,
            "productName": "",
            "productNum": 0,
            "productPacking": "",
            "productPv": 0.0,
            "productRetailPrice": 0.0,
            "productUnit": "",
            "updateTime": "",
        }
    ],  # 押货单商品列表信息
    "invtMortgageOrderVO": {
        "auditMan": "",
        "auditManId": 0,
        "auditRemarks": "",
        "auditStatus": 0,
        "companyCode": "",
        "createTime": "",
        "del": 0,
        "id": 0,
        "isDelivery": 0,
        "isLogisticsEvaluationReplied": 0,
        "isLogisticsFeedbackReplied": 0,
        "isTrafficControl": 0,
        "leaderNo": "",
        "logisticsEvaluation": 0,
        "logisticsFeedback": "",
        "orderMark": 0,
        "orderMortgageAmount": 0.0,
        "orderRetailAmount": 0.0,
        "orderSn": "",
        "orderSource": 0,
        "orderStatus": 0,
        "recordTime": "",
        "remarks": "",
        "storeCode": "",
        "storeId": 0,
        "submitMan": "",
        "submitManId": 0,
        "updateTime": "",
    },  # 押货单基本信息
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_addMortgageOrder(data=data, headers=headers):
    """
    运营后台添加押货单
    /mgmt/inventory/order/addMortgageOrder

    参数说明:
    - invtMortgageOrderProductVOList: 押货单商品列表信息
    - invtMortgageOrderProductVOList.del: 删除状态 0未删除 1已删除
    - invtMortgageOrderProductVOList.isGift: 是否为赠品 0否 1是
    - invtMortgageOrderProductVOList.orderId: 押货单id
    - invtMortgageOrderProductVOList.orderSn: 押货单号
    - invtMortgageOrderProductVOList.productBoxNum: 装箱数量
    - invtMortgageOrderProductVOList.productCode: 物品编号
    - invtMortgageOrderProductVOList.productDeliveredNum: 已发货数
    - invtMortgageOrderProductVOList.productId: 物品id
    - invtMortgageOrderProductVOList.productMortgagePrice: 物品押货价
    - invtMortgageOrderProductVOList.productName: 物品名称
    - invtMortgageOrderProductVOList.productNum: 押货数量
    - invtMortgageOrderProductVOList.productPacking: 物品规格
    - invtMortgageOrderProductVOList.productPv: 物品积分
    - invtMortgageOrderProductVOList.productRetailPrice: 物品零售价
    - invtMortgageOrderProductVOList.productUnit: 物品单位
    - invtMortgageOrderVO: 押货单基本信息
    - invtMortgageOrderVO.auditMan: 审批人
    - invtMortgageOrderVO.auditManId: 审批人id
    - invtMortgageOrderVO.auditRemarks: 审核备注
    - invtMortgageOrderVO.auditStatus: 审批状态 0不通过 1通过
    - invtMortgageOrderVO.companyCode: 分公司编号
    - invtMortgageOrderVO.del: 删除标识，0：未删除；1：已删除
    - invtMortgageOrderVO.isDelivery: 0不需要发货 1需要发货
    - invtMortgageOrderVO.isLogisticsEvaluationReplied: 是否已回复物流评价 0未回复 1已回复
    - invtMortgageOrderVO.isLogisticsFeedbackReplied: 是否已回复物流反馈 0未回复 1已回复
    - invtMortgageOrderVO.isTrafficControl: 是否处于交通管制 0否 1是
    - invtMortgageOrderVO.leaderNo: 负责人卡号
    - invtMortgageOrderVO.logisticsEvaluation: 物流评价 0未评价 1非常满意 2满意 3不满意
    - invtMortgageOrderVO.logisticsFeedback: 物流反馈(逗号隔开) 0未反馈 1延迟到货 2货损 3货差 4服务态度差
    - invtMortgageOrderVO.orderMark: 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    - invtMortgageOrderVO.orderMortgageAmount: 押货总金额
    - invtMortgageOrderVO.orderRetailAmount: 押货零售总金额
    - invtMortgageOrderVO.orderSn: 押货单号
    - invtMortgageOrderVO.orderSource: 押货单来源 1服务中心押货 2服务中心换货 3后台押货 4后台换货 5套装拆分押货 6套装组合押货
    - invtMortgageOrderVO.orderStatus: 1待审核 2待发货（审核通过） 3部分发货 4全部发货 5已收货 6已取消（审核不通过）
    - invtMortgageOrderVO.recordTime: 录单时间
    - invtMortgageOrderVO.remarks: 押货备注
    - invtMortgageOrderVO.storeCode: 店铺编号
    - invtMortgageOrderVO.storeId: 店铺id
    - invtMortgageOrderVO.submitMan: 经办人
    - invtMortgageOrderVO.submitManId: 经办人id
    - transId: 业务id
    """

    url = "/mgmt/inventory/order/addMortgageOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
