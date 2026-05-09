import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_split_detail_count(data=data, headers=headers):
    """
    套装拆分明细统计
    /appStore/dis-inventory/split/detail-count

    参数说明:
    - storeCode: 店铺编号
    """

    url = "/appStore/dis-inventory/split/detail-count"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
