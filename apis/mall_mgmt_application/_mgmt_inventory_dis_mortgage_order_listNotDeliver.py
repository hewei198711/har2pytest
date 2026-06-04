import os

from util.client import client

params = {
    "endTime": "",  # 结束提交时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 商品编号
    "startTime": "",  # 开始提交时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_listNotDeliver(params=params, headers=headers):
    """
    欠货未发列表查询
    /mgmt/inventory/dis/mortgage/order/listNotDeliver

    参数说明:
    - endTime: 结束提交时间
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 商品编号
    - startTime: 开始提交时间
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/order/listNotDeliver"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
