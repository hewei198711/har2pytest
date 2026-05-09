import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "endTime": "",  # 结束时间
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "orderSn": "",  # 换货单编号
    "orderStatus": 0,  # 状态: 1待审核 2待退回 3待验货 4待补换 5待收货 6已完成 7已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder_list(params=params, headers=headers):
    """
    换货单列表
    /appStore/purchaseExchangeOrder/list

    参数说明:
    - beginTime: 开始时间
    - endTime: 结束时间
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - orderSn: 换货单编号
    - orderStatus: 状态: 1待审核 2待退回 3待验货 4待补换 5待收货 6已完成 7已取消
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/purchaseExchangeOrder/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
