import os

from util.client import client

params = {
    "combineBegin": "",  # 组合开始时间
    "combineEnd": "",  # 组合结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_combine_record_page(params=params, headers=headers):
    """
    套装组合记录列表
    /appStore/dis-inventory/combine/record/page

    参数说明:
    - combineBegin: 组合开始时间
    - combineEnd: 组合结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号/名称
    """

    url = "/appStore/dis-inventory/combine/record/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
