import os

from util.client import client

data = {
    "crtlMan": "",  # 操作人
    "ctrlEndTime": "",  # 操作结束时间 yyyy-MM-dd
    "ctrlStartTime": "",  # 操作开始时间 yyyy-MM-dd
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_ctrlLogPageList(data=data, headers=headers):
    """
    操作日志
    /mgmt/inventory/distribution/ctrlLogPageList

    参数说明:
    - crtlMan: 操作人
    - ctrlEndTime: 操作结束时间 yyyy-MM-dd
    - ctrlStartTime: 操作开始时间 yyyy-MM-dd
    - pageNum: 第几页
    - pageSize: 页数
    - productCode: 产品编号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/distribution/ctrlLogPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
