import os

from util.client import client

data = {
    "creatorCard": "",  # 开单人卡号
    "creatorName": "",  # 开单人姓名
    "creatorPhone": "",  # 开单人手机
    "creatorType": 0,  # 开单人类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "creatorTypeList": [],  # 开单人类型集合
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "from": 0,  # TODO: 添加参数说明
    "fuzzyKey": "",  # 顾客卡号/顾客姓名/开单人姓名，模糊搜索
    "logStatus": 0,  # 状态 1->已生成 2->已作废
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payEndTime": "",  # 支付结束时间，格式：yyyy-MM-dd
    "payStartTime": "",  # 支付开始时间，格式：yyyy-MM-dd
    "promotionId": 0,  # 活动id
    "serialNo": "",  # 商品编码
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStoreGygEnergy(data=data, headers=headers):
    """
    店铺运营系统-门店能量流水
    /appStore/order/getStoreGygEnergy

    参数说明:
    - creatorCard: 开单人卡号
    - creatorName: 开单人姓名
    - creatorPhone: 开单人手机
    - creatorType: 开单人类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - creatorTypeList: 开单人类型集合
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - fuzzyKey: 顾客卡号/顾客姓名/开单人姓名，模糊搜索
    - logStatus: 状态 1->已生成 2->已作废
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - payEndTime: 支付结束时间，格式：yyyy-MM-dd
    - payStartTime: 支付开始时间，格式：yyyy-MM-dd
    - promotionId: 活动id
    - serialNo: 商品编码
    - storeCode: 服务中心编号
    """

    url = "/appStore/order/getStoreGygEnergy"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
