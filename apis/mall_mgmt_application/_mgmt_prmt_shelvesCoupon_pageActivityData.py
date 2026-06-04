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


def _mgmt_prmt_shelvesCoupon_pageActivityData(params=params, headers=headers):
    """
    分页查询活动数据
    /mgmt/prmt/shelvesCoupon/pageActivityData

    参数说明:
    - endTime: 数据时间止区
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTime: 数据时间起区
    """

    url = "/mgmt/prmt/shelvesCoupon/pageActivityData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
