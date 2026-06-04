import os

from util.client import client

data = {
    "chgContent": 0,  # 变更内容,0-全部，1-产品名称，2-销售主体，3-产品价格与pv
    "endTime": 0,  # 结束时间时间戳
    "operator": "",  # 操作人
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productId": "",  # 商品id
    "startTime": 0,  # 开始时间时间戳
    "versionId": "",  # 商品版本id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_listVerLog(data=data, headers=headers):
    """
    商品版本变更历史列表
    /mgmt/product/item/listVerLog

    参数说明:
    - chgContent: 变更内容,0-全部，1-产品名称，2-销售主体，3-产品价格与pv
    - endTime: 结束时间时间戳
    - operator: 操作人
    - pageNum: 页码
    - pageSize: 页面大小
    - productId: 商品id
    - startTime: 开始时间时间戳
    - versionId: 商品版本id
    """

    url = "/mgmt/product/item/listVerLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
