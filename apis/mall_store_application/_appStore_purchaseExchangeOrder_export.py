import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "endTime": "",  # 结束时间
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "orderSn": "",  # 换货单编号
    "orderStatus": 0,  # 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_export(params=params, headers=headers):
    """
    导出换货单列表
    /appStore/purchaseExchangeOrder/export

    参数说明:
    - beginTime: 开始时间
    - endTime: 结束时间
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - orderSn: 换货单编号
    - orderStatus: 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/appStore/purchaseExchangeOrder/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
