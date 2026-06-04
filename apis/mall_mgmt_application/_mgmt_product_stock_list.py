import os

from util.client import client

data = {
    "historyStatus": 0,  # 版本状态，1-待生效，2-生效中
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productTitle": "",  # 产品名称
    "serialNo": "",  # 产品编码
    "stockType": 0,  # 库存类型,0-全部,1-限量,2-非限量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_stock_list(data=data, headers=headers):
    """
    库存列表
    /mgmt/product/stock/list

    参数说明:
    - historyStatus: 版本状态，1-待生效，2-生效中
    - pageNum: 页码
    - pageSize: 页面大小
    - productTitle: 产品名称
    - serialNo: 产品编码
    - stockType: 库存类型,0-全部,1-限量,2-非限量
    """

    url = "/mgmt/product/stock/list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
