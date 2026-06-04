import os

from util.client import client

data = {
    "id": 0,  # id，可传空
    "performanceTarget": 0,  # 业绩目标
    "storeCode": "",  # 服务中心编号
    "year": 0,  # 业绩年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addOrUpdatePerformanceAppraisal(data=data, headers=headers):
    """
    新增/编辑服务中心业绩目标
    /mgmt/store/addOrUpdatePerformanceAppraisal

    参数说明:
    - id: id，可传空
    - performanceTarget: 业绩目标
    - storeCode: 服务中心编号
    - year: 业绩年份
    """

    url = "/mgmt/store/addOrUpdatePerformanceAppraisal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
