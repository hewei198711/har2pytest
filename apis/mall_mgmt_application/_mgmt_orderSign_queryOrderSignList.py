import os

from util.client import client

data = {
    "businessMode": 0,  # 经营模式 1->1:3  2->85%
    "companyCode": "",  # 业务分公司编号
    "companyCodes": [],  # 分公司编号
    "companyName": "",  # 业务分公司名称
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客卡号
    "deductionMode": 0,  # 签约购3.0使用，扣款方式，1：自主支付；2：自动扣款
    "endSignMonth": "",  # 签约结束时间
    "expressType": 0,  # 交付方式 1->服务中心自提 2->公司配送
    "financeCompanyCode": "",  # 财务分公司编号
    "isContinue": False,  # 是否续签单 true是 , false否
    "isFail": False,  # 是否曾经断点续签成功 true是 , false否
    "isUpgrade": 0,  # 是否为升级单 0->否 1->是
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payStage": 0,  # 已执行期数
    "payStageList": [],  # 已执行期数字符串，查多期。数组
    "payStageStr": "",  # 已执行期数字符串，查多期。 逗号分隔
    "payType": 0,  # 付款方式，1->一次性付款 2->分期付款
    "promId": "",  # 活动id
    "promotionId": "",  # 活动id
    "signNo": "",  # 签约单号
    "signOrderPayTypeList": [],  # 当月续约情况  1:已支付、2:未支付、3：已押货、4：未押货 不传值=全部
    "signPromTye": "",  # 签约购，类型
    "signQualification": 0,  # 当月续签资格 null->全部 0->无  1->有
    "signStatus": 0,  # 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->已取消 6->续约异常
    "signType": 0,  # 签约类型，1：2.0；2：3.0
    "signWay": 0,  # 购买方式 1->自购 2->代购
    "source": 0,  # 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    "startSignMonth": "",  # 签约开始时间
    "storeCancel": 0,  # 门店是否结点  0->否 1->是
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_queryOrderSignList(data=data, headers=headers):
    """
    报表中心> 签约管理报表-列表
    /mgmt/orderSign/queryOrderSignList

    参数说明:
    - businessMode: 经营模式 1->1:3  2->85%
    - companyCode: 业务分公司编号
    - companyCodes: 分公司编号
    - companyName: 业务分公司名称
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - deductionMode: 签约购3.0使用，扣款方式，1：自主支付；2：自动扣款
    - endSignMonth: 签约结束时间
    - expressType: 交付方式 1->服务中心自提 2->公司配送
    - financeCompanyCode: 财务分公司编号
    - isContinue: 是否续签单 true是 , false否
    - isFail: 是否曾经断点续签成功 true是 , false否
    - isUpgrade: 是否为升级单 0->否 1->是
    - pageNum: 页数
    - pageSize: 每页显示数
    - payStage: 已执行期数
    - payStageList: 已执行期数字符串，查多期。数组
    - payStageStr: 已执行期数字符串，查多期。 逗号分隔
    - payType: 付款方式，1->一次性付款 2->分期付款
    - promId: 活动id
    - promotionId: 活动id
    - signNo: 签约单号
    - signOrderPayTypeList: 当月续约情况  1:已支付、2:未支付、3：已押货、4：未押货 不传值=全部
    - signPromTye: 签约购，类型
    - signQualification: 当月续签资格 null->全部 0->无  1->有
    - signStatus: 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->已取消 6->续约异常
    - signType: 签约类型，1：2.0；2：3.0
    - signWay: 购买方式 1->自购 2->代购
    - source: 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    - startSignMonth: 签约开始时间
    - storeCancel: 门店是否结点  0->否 1->是
    - storeCode: 服务中心编号
    """

    url = "/mgmt/orderSign/queryOrderSignList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
