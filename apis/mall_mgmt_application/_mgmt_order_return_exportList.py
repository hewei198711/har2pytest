import os

from util.client import client

data = {
    "applySource": 0,  # 申请来源 0 >代客售后 1->顾客申请 2->代顾客申请 3->商城1.0申请 4-系统自动退款
    "applyTimeBegin": "",  # 申请开始时间 #格式yyyy-MM-dd
    "applyTimeEnd": "",  # 申请结束时间 #格式yyyy-MM-dd
    "businessMode": 0,  # 经营模式 1->1:3押货 2->85折押货
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号
    "companyName": "",  # 分公司名称
    "completeTimeBegin": "",  # 退货完成开始时间 #格式yyyy-MM-dd
    "completeTimeEnd": "",  # 退货完成结束时间 #格式yyyy-MM-dd
    "confirmPerson": "",  # 入仓确认人
    "confirmStatus": 0,  # 入仓确认状态 0->待确认 1->已确认
    "confirmTimeBegin": "",  # 入仓确认开始时间 #格式yyyy-MM-dd
    "confirmTimeEnd": "",  # 入仓确认结束时间 #格式yyyy-MM-dd
    "creatorCard": "",  # 开单人卡号
    "creatorId": 0,  # 开单人id
    "creatorTypes": [],  # 开单人类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "customerCard": "",  # 顾客卡号
    "customerId": 0,  # 顾客id
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "customerTypes": [],  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "depositNo": "",  # 对应定金订单号
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "financeCompanyCode": "",  # 财务分公司编号
    "financeCompanyCodes": [],  # 财务分公司编号
    "financeCompanyName": "",  # 财务分公司名称
    "isDeliver": 0,  # 是否发货 0->不发货 1->发货
    "isDisSelfStoreOrder": 0,  # 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    "isUpgrade": 0,  # 是否升级单 0->否 1->是
    "orderDeliverStatus": 0,  # 订单发货状态 0->待发货 1->已发货 2->不需发货
    "orderNo": "",  # 订单编号
    "orderTypes": [],  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9-> 签约购转分订单 10-> 配件订单 12-礼物订单
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "productOrderTypes": [],  # 订货类型： 1-产品订货 2-资料订货 3-定制品订货 4-赠品领取 5-配件订货
    "pushStatus": 0,  # 入仓推送状态 0->待推送 1->已推送，传这个字段时同时传confirmStatus=1
    "returnExpressType": 0,  # 退回方式  1->物流发货 2->顾客自带 3->上门取件
    "returnInvoiceStatus": 0,  # 退票状态  1->待退票 2->已退票 3->已取消
    "returnNo": "",  # 退货单号
    "returnStatus": 0,  # 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    "returnType": 0,  # 退货类型 1->当月退货 2->隔月退货
    "stockTypeList": [],  # 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "userCard": "",  # 用户卡号
    "waitAuditType": 0,  # 待审核类型  1->待服务中心审核 2->待分公司审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_exportList(data=data, headers=headers):
    """
    退货列表批量导出
    /mgmt/order/return/exportList

    参数说明:
    - applySource: 申请来源 0 >代客售后 1->顾客申请 2->代顾客申请 3->商城1.0申请 4-系统自动退款
    - applyTimeBegin: 申请开始时间 #格式yyyy-MM-dd
    - applyTimeEnd: 申请结束时间 #格式yyyy-MM-dd
    - businessMode: 经营模式 1->1:3押货 2->85折押货
    - companyCode: 分公司编号
    - companyCodes: 分公司编号
    - companyName: 分公司名称
    - completeTimeBegin: 退货完成开始时间 #格式yyyy-MM-dd
    - completeTimeEnd: 退货完成结束时间 #格式yyyy-MM-dd
    - confirmPerson: 入仓确认人
    - confirmStatus: 入仓确认状态 0->待确认 1->已确认
    - confirmTimeBegin: 入仓确认开始时间 #格式yyyy-MM-dd
    - confirmTimeEnd: 入仓确认结束时间 #格式yyyy-MM-dd
    - creatorCard: 开单人卡号
    - creatorId: 开单人id
    - creatorTypes: 开单人类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - customerCard: 顾客卡号
    - customerId: 顾客id
    - customerPhone: 顾客手机号
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - customerTypes: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - depositNo: 对应定金订单号
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - financeCompanyCode: 财务分公司编号
    - financeCompanyCodes: 财务分公司编号
    - financeCompanyName: 财务分公司名称
    - isDeliver: 是否发货 0->不发货 1->发货
    - isDisSelfStoreOrder: 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    - isUpgrade: 是否升级单 0->否 1->是
    - orderDeliverStatus: 订单发货状态 0->待发货 1->已发货 2->不需发货
    - orderNo: 订单编号
    - orderTypes: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9-> 签约购转分订单 10-> 配件订单 12-礼物订单
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 每页显示数
    - productOrderTypes: 订货类型： 1-产品订货 2-资料订货 3-定制品订货 4-赠品领取 5-配件订货
    - pushStatus: 入仓推送状态 0->待推送 1->已推送，传这个字段时同时传confirmStatus=1
    - returnExpressType: 退回方式  1->物流发货 2->顾客自带 3->上门取件
    - returnInvoiceStatus: 退票状态  1->待退票 2->已退票 3->已取消
    - returnNo: 退货单号
    - returnStatus: 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    - returnType: 退货类型 1->当月退货 2->隔月退货
    - stockTypeList: 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - userCard: 用户卡号
    - waitAuditType: 待审核类型  1->待服务中心审核 2->待分公司审核
    """

    url = "/mgmt/order/return/exportList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
