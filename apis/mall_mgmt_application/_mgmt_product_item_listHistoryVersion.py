import os

from util.client import client

data = {
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productId": "",  # 商品id
    "serialNo": "",  # 商品编码
    "startTime": 0,  # 开始时间时间戳
    "title": "",  # 商品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_listHistoryVersion(data=data, headers=headers):
    """
    商品版本历史列表
    /mgmt/product/item/listHistoryVersion

    参数说明:
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 页面大小
    - productId: 商品id
    - serialNo: 商品编码
    - startTime: 开始时间时间戳
    - title: 商品名称
    """

    url = "/mgmt/product/item/listHistoryVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
