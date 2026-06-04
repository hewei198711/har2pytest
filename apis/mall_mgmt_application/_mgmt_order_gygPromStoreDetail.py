import os

from util.client import client

data = {
    "creatorTypeList": [],  # 开单人类型集合
    "energyRangeEnd": 0.0,  # 能量范围，结束值
    "energyRangeStart": 0.0,  # 能量范围，开始值
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payEndTime": "",  # 支付结束时间，格式：yyyy-MM
    "payStartTime": "",  # 支付开始时间，格式：yyyy-MM
    "promotionId": 0,  # 活动id
    "shopkeeperCard": "",  # 管理人会员卡号
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_gygPromStoreDetail(data=data, headers=headers):
    """
    公益购活动详情-门店数据情况
    /mgmt/order/gygPromStoreDetail

    参数说明:
    - creatorTypeList: 开单人类型集合
    - energyRangeEnd: 能量范围，结束值
    - energyRangeStart: 能量范围，开始值
    - pageNum: 页数
    - pageSize: 每页显示数
    - payEndTime: 支付结束时间，格式：yyyy-MM
    - payStartTime: 支付开始时间，格式：yyyy-MM
    - promotionId: 活动id
    - shopkeeperCard: 管理人会员卡号
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/order/gygPromStoreDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
