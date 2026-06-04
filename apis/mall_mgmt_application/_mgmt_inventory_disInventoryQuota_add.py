import os

from util.client import client

data = {
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "quota": 0.0,  # 库存限额
    "storeCode": "",  # 服务中心编号
    "storeType": "",  # 网点类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_add(data=data, headers=headers):
    """
    新增/编辑,只需要传服务中心编号和限额
    /mgmt/inventory/disInventoryQuota/add

    参数说明:
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - quota: 库存限额
    - storeCode: 服务中心编号
    - storeType: 网点类型
    """

    url = "/mgmt/inventory/disInventoryQuota/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
