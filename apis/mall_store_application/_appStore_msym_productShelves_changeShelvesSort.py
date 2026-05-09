import os

from util.client import client

data = {
    "productShelvesKeyword": "",  # 货架关联关联词
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_productShelves_changeShelvesSort(data=data, headers=headers):
    """
    修改对应货架的排序
    /appStore/msym/productShelves/changeShelvesSort

    参数说明:
    - productShelvesKeyword: 货架关联关联词
    - sort: 排序
    """

    url = "/appStore/msym/productShelves/changeShelvesSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
