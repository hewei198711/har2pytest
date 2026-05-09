import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_combine_page(params=params, headers=headers):
    """
    套装组合列表
    /appStore/inventory/combine/page

    参数说明:
    - beginTime: 开始时间
    - endTime: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号/名称
    """

    url = "/appStore/inventory/combine/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
