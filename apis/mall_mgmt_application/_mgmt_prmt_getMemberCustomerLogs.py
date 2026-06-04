import os

from util.client import client

data = {
    "createTimeMax": "",  # 编辑时间末
    "createTimeMin": "",  # 编辑时间始
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getMemberCustomerLogs(data=data, headers=headers):
    """
    查询自定义顾客修改记录列表
    /mgmt/prmt/getMemberCustomerLogs

    参数说明:
    - createTimeMax: 编辑时间末
    - createTimeMin: 编辑时间始
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/getMemberCustomerLogs"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
