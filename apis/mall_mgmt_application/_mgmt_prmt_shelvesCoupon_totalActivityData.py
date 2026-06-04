import os

from util.client import client

params = {
    "endTime": "",  # 数据时间止区
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTime": "",  # 数据时间起区
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_totalActivityData(params=params, headers=headers):
    """
    累计数据统计
    /mgmt/prmt/shelvesCoupon/totalActivityData

    参数说明:
    - endTime: 数据时间止区
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTime: 数据时间起区
    """

    url = "/mgmt/prmt/shelvesCoupon/totalActivityData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
