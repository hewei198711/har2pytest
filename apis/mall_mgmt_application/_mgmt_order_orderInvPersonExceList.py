import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请结束时间yyyy-MM-dd HH:mm:ss
    "applyStartTime": "",  # 申请开始时间yyyy-MM-dd HH:mm:ss
    "auditStatus": 0,  # 审核状态 1->待审核 2->已通过 3->已驳回
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客会员卡
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "financeCompanyCode": "",  # 财务分公司编号
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编号
    "orderStatus": 0,  # 订单状态  -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderInvPersonExceList(data=data, headers=headers):
    """
    异常个人要票订单列表
    /mgmt/order/orderInvPersonExceList

    参数说明:
    - applyEndTime: 申请结束时间yyyy-MM-dd HH:mm:ss
    - applyStartTime: 申请开始时间yyyy-MM-dd HH:mm:ss
    - auditStatus: 审核状态 1->待审核 2->已通过 3->已驳回
    - creatorCard: 开单人卡号
    - customerCard: 顾客会员卡
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - financeCompanyCode: 财务分公司编号
    - orderNo: 订单编号
    - orderStatus: 订单状态  -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/order/orderInvPersonExceList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
