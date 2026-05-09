import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_combine_page(params=params, headers=headers):
    """
    套装组合列表
    /appStore/dis-inventory/combine/page

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号/名称
    """

    url = "/appStore/dis-inventory/combine/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
