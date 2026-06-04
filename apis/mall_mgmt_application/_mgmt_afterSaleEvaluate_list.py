import os

from util.client import client

data = {
    "afterSaleNo": "",  # 售后单号
    "companyCode": "",  # 业务分公司编号
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客卡号
    "endCreateTime": "",  # 评价时间-结束时间
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "isEvaluate": False,  # 是否评价 0:未评价 , 1:已评价
    "isSystem": 0,  # 是否系统自动评价 0否, 1是
    "orderDeliverStatus": 0,  # 订单发货状态 0->待发货 1->已发货 2->不需发货
    "orderTypes": [],  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9-> 签约购转分订单 10-> 配件订单
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serviceAttitude": 0,  # 服务态度 1=不满意,2=一般, 3=满意,4=非常满意
    "serviceConvenience": 0,  # 服务便捷度  1=不满意,2=一般, 3=满意,4=非常满意
    "serviceHours": 0,  # 服务时效  1=不满意,2=一般, 3=满意,4=非常满意
    "serviceLogistics": 0,  # 售后物流评价 1=不满意,2=一般, 3=满意,4=非常满意
    "startCreateTime": "",  # 评价时间-开始时间
    "type": 0,  # 类型 1=退货,2=换货,3=货损货差,4=维修,5=返厂维修
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterSaleEvaluate_list(data=data, headers=headers):
    """
    售后评价列表
    /mgmt/afterSaleEvaluate/list

    参数说明:
    - afterSaleNo: 售后单号
    - companyCode: 业务分公司编号
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - endCreateTime: 评价时间-结束时间
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - isEvaluate: 是否评价 0:未评价 , 1:已评价
    - isSystem: 是否系统自动评价 0否, 1是
    - orderDeliverStatus: 订单发货状态 0->待发货 1->已发货 2->不需发货
    - orderTypes: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9-> 签约购转分订单 10-> 配件订单
    - pageNum: 页码
    - pageSize: 页面大小
    - serviceAttitude: 服务态度 1=不满意,2=一般, 3=满意,4=非常满意
    - serviceConvenience: 服务便捷度  1=不满意,2=一般, 3=满意,4=非常满意
    - serviceHours: 服务时效  1=不满意,2=一般, 3=满意,4=非常满意
    - serviceLogistics: 售后物流评价 1=不满意,2=一般, 3=满意,4=非常满意
    - startCreateTime: 评价时间-开始时间
    - type: 类型 1=退货,2=换货,3=货损货差,4=维修,5=返厂维修
    """

    url = "/mgmt/afterSaleEvaluate/list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
