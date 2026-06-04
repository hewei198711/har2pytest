import os

from util.client import client

data = {
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productId": 0,  # 商品id
    "startTime": 0,  # 开始时间时间戳
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_getAuditLog(data=data, headers=headers):
    """
    分公司价格信息操作日志
    /mgmt/product/filiale/getAuditLog

    参数说明:
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 页面大小
    - productId: 商品id
    - startTime: 开始时间时间戳
    """

    url = "/mgmt/product/filiale/getAuditLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
