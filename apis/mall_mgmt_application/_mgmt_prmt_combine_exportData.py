import os

from util.client import client

params = {
    "endTime": "",  # 结束时间(yyyy-MM-dd)
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "startTime": "",  # 开始时间(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_exportData(params=params, headers=headers):
    """
    导出活动数据明细
    /mgmt/prmt/combine/exportData

    参数说明:
    - endTime: 结束时间(yyyy-MM-dd)
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页条数
    - startTime: 开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/combine/exportData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
