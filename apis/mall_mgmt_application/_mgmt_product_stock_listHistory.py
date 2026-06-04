import os

from util.client import client

data = {
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "startTime": 0,  # 开始时间时间戳
    "stockId": 0,  # 库存id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_stock_listHistory(data=data, headers=headers):
    """
    库存历史
    /mgmt/product/stock/listHistory

    参数说明:
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 页面大小
    - startTime: 开始时间时间戳
    - stockId: 库存id
    """

    url = "/mgmt/product/stock/listHistory"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
