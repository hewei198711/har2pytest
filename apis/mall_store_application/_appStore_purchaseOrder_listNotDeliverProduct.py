import os

from util.client import client

params = {
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号或产品名称模糊查询参数
    "startTime": "",  # 开始时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_listNotDeliverProduct(params=params, headers=headers):
    """
    获取欠货未发列表
    /appStore/purchaseOrder/listNotDeliverProduct

    参数说明:
    - endTime: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号或产品名称模糊查询参数
    - startTime: 开始时间
    - storeCode: 服务中心编号
    """

    url = "/appStore/purchaseOrder/listNotDeliverProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
