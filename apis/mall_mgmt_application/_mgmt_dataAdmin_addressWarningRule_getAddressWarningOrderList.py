import os

from util.client import client

params = {
    "creatorCard": "",  # 开单人卡号
    "creatorPhone": "",  # 开单人手机
    "customerCard": "",  # 顾客卡号
    "customerPhone": "",  # 顾客手机号
    "deliverStoreCode": "",  # 顾客交付服务中心编号
    "detailedAddress": "",  # 收货地址
    "orderNo": "",  # 订单编号
    "orderStatus": 0,  # 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 99->已完成
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # 报单月份
    "placeMonthStr": "",  # 报单月份(前端传参)
    "receiverPhone": "",  # 收货人手机号
    "ruleEndTime": "",  # 规则结束时间
    "ruleId": 0,  # 规则id
    "ruleStartTime": "",  # 规则开始时间
    "storeCode": "",  # 归属服务中心编号
    "storeName": "",  # 归属服务中心名称
    "warningType": 0,  # 预警方式(0:地址预警；1：电话预警；2：两者都预警)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_addressWarningRule_getAddressWarningOrderList(params=params, headers=headers):
    """
    根据ruleId获取预警订单明细
    /mgmt/dataAdmin/addressWarningRule/getAddressWarningOrderList

    参数说明:
    - creatorCard: 开单人卡号
    - creatorPhone: 开单人手机
    - customerCard: 顾客卡号
    - customerPhone: 顾客手机号
    - deliverStoreCode: 顾客交付服务中心编号
    - detailedAddress: 收货地址
    - orderNo: 订单编号
    - orderStatus: 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 99->已完成
    - placeMonth: 报单月份
    - placeMonthStr: 报单月份(前端传参)
    - receiverPhone: 收货人手机号
    - ruleEndTime: 规则结束时间
    - ruleId: 规则id
    - ruleStartTime: 规则开始时间
    - storeCode: 归属服务中心编号
    - storeName: 归属服务中心名称
    - warningType: 预警方式(0:地址预警；1：电话预警；2：两者都预警)
    """

    url = "/mgmt/dataAdmin/addressWarningRule/getAddressWarningOrderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
