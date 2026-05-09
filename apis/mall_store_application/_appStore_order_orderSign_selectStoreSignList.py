import os

from util.client import client

data = {
    "customerCard": "",  # 签约顾客卡号
    "customerName": "",  # 签约顾客姓名
    "deliveryMethod": 0,  # 交付方式（枚举）：1->门店交付，2->公司交付
    "monthlyPayment": [],  # 本月支付情况（枚举），例如：1->本月已支付，2->本月未支付，3->本月已押货，4->本月未押货，5-本月未审核，6-本月已审核
    "monthlyRenewQualification": 0,  # 本月续签资格（枚举）：1->有，0->无
    "ongoing": 0,  # 是否查询正在进行（枚举）：1->是，0->否
    "orderNo": "",  # 订单号，本月未审核才有值
    "pageNum": 0,  # 分页页码
    "pageSize": 0,  # 分页页大小
    "payMethod": 0,  # 支付方式（枚举）：1->自主支付，2->自动扣款
    "signMethod": 0,  # 签约方式（枚举）：1->一次性付款，2->分期付款
    "signNo": "",  # 签约购单号
    "signProgress": 0,  # 签约进度（数值型）
    "signStatusList": [],  # 签约状态（下拉多选），传入多个状态码
    "signTimeEnd": "",  # 签约时间结束，格式：yyyy-MM-dd
    "signTimeStart": "",  # 签约时间开始，格式：yyyy-MM-dd
    "signWay": 0,  # 下单方式 1->顾客自购 2->代客签约
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_selectStoreSignList(data=data, headers=headers):
    """
    店铺运营系统-签约购管理列表-new
    /appStore/order/orderSign/selectStoreSignList

    参数说明:
    - customerCard: 签约顾客卡号
    - customerName: 签约顾客姓名
    - deliveryMethod: 交付方式（枚举）：1->门店交付，2->公司交付
    - monthlyPayment: 本月支付情况（枚举），例如：1->本月已支付，2->本月未支付，3->本月已押货，4->本月未押货，5-本月未审核，6-本月已审核
    - monthlyRenewQualification: 本月续签资格（枚举）：1->有，0->无
    - ongoing: 是否查询正在进行（枚举）：1->是，0->否
    - orderNo: 订单号，本月未审核才有值
    - pageNum: 分页页码
    - pageSize: 分页页大小
    - payMethod: 支付方式（枚举）：1->自主支付，2->自动扣款
    - signMethod: 签约方式（枚举）：1->一次性付款，2->分期付款
    - signNo: 签约购单号
    - signProgress: 签约进度（数值型）
    - signStatusList: 签约状态（下拉多选），传入多个状态码
    - signTimeEnd: 签约时间结束，格式：yyyy-MM-dd
    - signTimeStart: 签约时间开始，格式：yyyy-MM-dd
    - signWay: 下单方式 1->顾客自购 2->代客签约
    """

    url = "/appStore/order/orderSign/selectStoreSignList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
