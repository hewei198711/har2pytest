import os

from util.client import client

data = {
    "createEndDate": "",  # 创建时间结束 yyyy-MM-dd
    "createStartDate": "",  # 创建时间开始 yyyy-MM-dd
    "operatorNo": "",  # 操作人工号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_recordList(data=data, headers=headers):
    """
    操作日志列表
    /mgmt/inventory/disInventoryQuota/recordList

    参数说明:
    - createEndDate: 创建时间结束 yyyy-MM-dd
    - createStartDate: 创建时间开始 yyyy-MM-dd
    - operatorNo: 操作人工号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/disInventoryQuota/recordList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
