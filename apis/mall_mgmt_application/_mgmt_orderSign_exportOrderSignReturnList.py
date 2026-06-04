import os

from util.client import client

data = {
    "belongGear": 0,  # 所属档位
    "businessMode": 0,  # 保证金类型 1->1:3押货 2->85折押货
    "companyCode": "",  # 业务分公司编号
    "companyCodes": [],  # 分公司编号
    "companyName": "",  # 业务分公司名称
    "creatorCard": "",  # 开单人卡号
    "creatorName": "",  # 开单人姓名
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # (顾客身份)顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "deductionMode": 0,  # 扣款方式，1：自主支付；2：自动扣款
    "endPayTime": "",  # 签约结束时间
    "expressType": 0,  # 交付方式 1->门店自提 2->公司交付
    "isContinue": False,  # 是否续签单 true是 , false否
    "isFail": False,  # 是否参与断点续签 true是 , false否
    "isUpgrade": 0,  # 是否需要升级 0->否 1->是
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payStage": 0,  # 已执行期数
    "payStageList": [],  # 已执行期数字符串，查多期。数组
    "payStageStr": "",  # 已执行期数字符串，查多期。 逗号分隔
    "payType": 0,  # (签约方式)付款方式，1->一次性付款 2->分期付款
    "promId": "",  # 活动id
    "promotionId": "",  # 活动id
    "signAmount": 0.0,  # (签约金额)1:3 首月订单的应付金额; 分级押货 首月转分单的应付金额
    "signNo": "",  # 签约单号
    "signOrderPayTypeList": [],  # 当月续约情况  1:已支付、2:未支付、3：已押货、4：未押货 不传值=全部
    "signPromTye": "",  # 签约购，类型
    "signQualification": 0,  # 当月续签资格 null->全部 0->无  1->有
    "signStatus": 0,  # 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    "signType": 0,  # 签约类型，1:2.0；2：3.0；3：4.0
    "signWay": 0,  # (下单方式)签约方式 1->自购 2->代购
    "source": 0,  # 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    "startPayTime": "",  # 签约开始时间
    "storeCancel": 0,  # 门店是否结点  0->否 1->是
    "storeCode": "",  # (门店编号)服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_exportOrderSignReturnList(data=data, headers=headers):
    """
    签约售后列表-导出
    /mgmt/orderSign/exportOrderSignReturnList

    参数说明:
    - belongGear: 所属档位
    - businessMode: 保证金类型 1->1:3押货 2->85折押货
    - companyCode: 业务分公司编号
    - companyCodes: 分公司编号
    - companyName: 业务分公司名称
    - creatorCard: 开单人卡号
    - creatorName: 开单人姓名
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerType: (顾客身份)顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - deductionMode: 扣款方式，1：自主支付；2：自动扣款
    - endPayTime: 签约结束时间
    - expressType: 交付方式 1->门店自提 2->公司交付
    - isContinue: 是否续签单 true是 , false否
    - isFail: 是否参与断点续签 true是 , false否
    - isUpgrade: 是否需要升级 0->否 1->是
    - pageNum: 页数
    - pageSize: 每页显示数
    - payStage: 已执行期数
    - payStageList: 已执行期数字符串，查多期。数组
    - payStageStr: 已执行期数字符串，查多期。 逗号分隔
    - payType: (签约方式)付款方式，1->一次性付款 2->分期付款
    - promId: 活动id
    - promotionId: 活动id
    - signAmount: (签约金额)1:3 首月订单的应付金额; 分级押货 首月转分单的应付金额
    - signNo: 签约单号
    - signOrderPayTypeList: 当月续约情况  1:已支付、2:未支付、3：已押货、4：未押货 不传值=全部
    - signPromTye: 签约购，类型
    - signQualification: 当月续签资格 null->全部 0->无  1->有
    - signStatus: 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    - signType: 签约类型，1:2.0；2：3.0；3：4.0
    - signWay: (下单方式)签约方式 1->自购 2->代购
    - source: 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    - startPayTime: 签约开始时间
    - storeCancel: 门店是否结点  0->否 1->是
    - storeCode: (门店编号)服务中心编号
    """

    url = "/mgmt/orderSign/exportOrderSignReturnList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
