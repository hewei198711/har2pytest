import os

from util.client import client

data = {
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "product": "",  # 套装产品编码/名称
    "splitBegin": "",  # 拆分时间
    "splitEnd": "",  # 拆分时间
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_split_record_page(data=data, headers=headers):
    """
    查询套装拆分记录列表
    /appStore/dis-inventory/split/record/page

    参数说明:
    - product: 套装产品编码/名称
    - splitBegin: 拆分时间
    - splitEnd: 拆分时间
    - storeCode: 店铺编号
    """

    url = "/appStore/dis-inventory/split/record/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
