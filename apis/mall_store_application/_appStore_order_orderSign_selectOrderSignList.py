import os

from util.client import client

data = {
    "businessMode": 0,  # 经营模式 1->1:3  2->85%
    "currentProductName": "",  # 当前产品
    "currentStage": 0,  # 签约进度
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "deductionMode": 0,  # 签约购3.0使用，扣款方式，1：自主支付；2：自动扣款；null：查全部
    "endPayTime": "",  # 签约结束时间
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "keyWord": "",  # 签约单号模糊,顾客姓名模糊
    "orderStatus": 0,  # 当月续约情况  1:已支付、2:未支付
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payType": 0,  # 付款方式，1->一次性付款 2->分期付款
    "promId": "",  # 活动id
    "promotionId": "",  # 活动id
    "signNo": "",  # 签约单号
    "signOrderPayType": 0,  # 本月支付情况 已签约状态下 1:已支付、2:未支付、3：已押货、4：未押货、null：查全部
    "signOrderPayTypeList": [],  # 本月支付情况 已签约状态下 1->本月已支付；2->本月未支付；3->本月已押货；4->本月未押货
    "signPromTye": "",  # 签约购，类型
    "signQualification": 0,  # 当月续签资格 null->全部 0->无  1->有
    "signStatus": 0,  # 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    "signStatusList": [],  # 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    "signType": 0,  # 签约类型，1：2.0；2：3.0
    "signWay": 0,  # 下单方式 1->顾客自购 2->代客签约
    "startPayTime": "",  # 签约开始时间
    "storeCode": "",  # 服务中心编号（服务中心自提）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_selectOrderSignList(data=data, headers=headers):
    """
    店铺运营系统-签约购管理列表
    /appStore/order/orderSign/selectOrderSignList

    参数说明:
    - businessMode: 经营模式 1->1:3  2->85%
    - currentProductName: 当前产品
    - currentStage: 签约进度
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - deductionMode: 签约购3.0使用，扣款方式，1：自主支付；2：自动扣款；null：查全部
    - endPayTime: 签约结束时间
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - keyWord: 签约单号模糊,顾客姓名模糊
    - orderStatus: 当月续约情况  1:已支付、2:未支付
    - pageNum: 页数
    - pageSize: 每页显示数
    - payType: 付款方式，1->一次性付款 2->分期付款
    - promId: 活动id
    - promotionId: 活动id
    - signNo: 签约单号
    - signOrderPayType: 本月支付情况 已签约状态下 1:已支付、2:未支付、3：已押货、4：未押货、null：查全部
    - signOrderPayTypeList: 本月支付情况 已签约状态下 1->本月已支付；2->本月未支付；3->本月已押货；4->本月未押货
    - signPromTye: 签约购，类型
    - signQualification: 当月续签资格 null->全部 0->无  1->有
    - signStatus: 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    - signStatusList: 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    - signType: 签约类型，1：2.0；2：3.0
    - signWay: 下单方式 1->顾客自购 2->代客签约
    - startPayTime: 签约开始时间
    - storeCode: 服务中心编号（服务中心自提）
    """

    url = "/appStore/order/orderSign/selectOrderSignList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
