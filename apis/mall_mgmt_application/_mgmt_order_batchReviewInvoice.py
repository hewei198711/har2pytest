import os

from util.client import client

data = {
    "applyTime": "",  # 申请时间
    "applyTimeDesc": "",  # TODO: 添加参数说明
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "expressType": 0,  # 交付方式 1->服务中心自提 2->公司配送
    "expressTypeDesc": "",  # TODO: 添加参数说明
    "financeCompanyCode": "",  # 财务分公司编号
    "invoiceType": 0,  # 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票
    "invoiceTypeDesc": "",  # TODO: 添加参数说明
    "isAcrossMonth": 0,  # 是否跨月(6月支付8月为跨月) 0->否 1->是
    "isReturn": 0,  # 是否退货 0->否 1->是
    "name": "",  # 个人姓名&单位全称
    "operateTime": "",  # 操作时间
    "operateTimeDesc": "",  # TODO: 添加参数说明
    "operator": "",  # 操作人
    "orderInvoiceId": 0,  # 主表id
    "orderNo": "",  # 订单号
    "orderNos": [],  # 订单号列表
    "orderStatus": 0,  # 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退款 99->已完成
    "orderStatusDesc": "",  # TODO: 添加参数说明
    "payTime": "",  # 付款时间
    "payTimeDesc": "",  # TODO: 添加参数说明
    "remarks": "",  # 备注
    "reviewStatus": 0,  # 审核状态 1->待审核 2->已通过 3->已驳回
    "reviewStatusDesc": "",  # TODO: 添加参数说明
    "totalAmount": 0.0,  # 实付金额=订单金额-返还金额-优惠券-电子礼券-运费补贴券+运费
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_batchReviewInvoice(data=data, headers=headers):
    """
    隔月开票批量审核
    /mgmt/order/batchReviewInvoice

    参数说明:
    - applyTime: 申请时间
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - expressType: 交付方式 1->服务中心自提 2->公司配送
    - financeCompanyCode: 财务分公司编号
    - invoiceType: 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票
    - isAcrossMonth: 是否跨月(6月支付8月为跨月) 0->否 1->是
    - isReturn: 是否退货 0->否 1->是
    - name: 个人姓名&单位全称
    - operateTime: 操作时间
    - operator: 操作人
    - orderInvoiceId: 主表id
    - orderNo: 订单号
    - orderNos: 订单号列表
    - orderStatus: 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退款 99->已完成
    - payTime: 付款时间
    - remarks: 备注
    - reviewStatus: 审核状态 1->待审核 2->已通过 3->已驳回
    - totalAmount: 实付金额=订单金额-返还金额-优惠券-电子礼券-运费补贴券+运费
    """

    url = "/mgmt/order/batchReviewInvoice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
