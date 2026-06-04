import os

from util.client import client

data = {
    "storeCode": "",  # 服务中心编号
    "serialNo": "",  # 产品编号
    "amount": 0,  # 保留数量
    "reserveBeginTime": 0,  # 保留开始时间戳
    "reserveEndTime": 0,  # 保留结束时间戳
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_saveReserveBundle(data=data, headers=headers):
    """
    新建或修改套装保留
    /mgmt/product/bundle/saveReserveBundle

    参数说明:
    - storeCode: 服务中心编号
    - serialNo: 产品编号
    - amount: 保留数量
    - reserveBeginTime: 保留开始时间戳
    - reserveEndTime: 保留结束时间戳
    """

    url = "/mgmt/product/bundle/saveReserveBundle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
