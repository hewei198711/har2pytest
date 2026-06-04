import os

from util.client import client

data = {
    "storeCode": "",  # 服务中心编号
    "productCode": "",  # 产品编号
    "amount": 0,  # 保留数量
    "beginTime": "",  # 保留开始时间戳
    "endTime": "",  # 保留结束时间戳
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_reverse_save(data=data, headers=headers):
    """
    新建或修改套装保留
    /mgmt/dis-inventory/split/reverse/save

    参数说明:
    - storeCode: 服务中心编号
    - productCode: 产品编号
    - amount: 保留数量
    - beginTime: 保留开始时间戳
    - endTime: 保留结束时间戳
    """

    url = "/mgmt/dis-inventory/split/reverse/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
