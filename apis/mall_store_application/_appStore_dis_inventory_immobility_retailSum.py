import os

from util.client import client

params = {
    "beginImmobilityTime": "",  # 不动库存开始时间
    "endImmobilityTime": "",  # 不动库存结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品关键字（编号或名称）
    "stock": 0,  # 库存
    "stockOperator": 0,  # 库存运算符: 1为'>='，2为'>'，3为'<=',4为'<'
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_immobility_retailSum(params=params, headers=headers):
    """
    库存总合计(长期不动库存维度)
    /appStore/dis-inventory/immobility/retailSum

    参数说明:
    - beginImmobilityTime: 不动库存开始时间
    - endImmobilityTime: 不动库存结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品关键字（编号或名称）
    - stock: 库存
    - stockOperator: 库存运算符: 1为'>='，2为'>'，3为'<=',4为'<'
    """

    url = "/appStore/dis-inventory/immobility/retailSum"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
