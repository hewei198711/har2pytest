import os

from util.client import client

params = {
    "endTime": "",  # 数据时间止区(yyyy-MM-dd)
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTime": "",  # 数据时间起区(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_pageData(params=params, headers=headers):
    """
    分页查询数据明细
    /mgmt/prmt/shoppedGift/pageData

    参数说明:
    - endTime: 数据时间止区(yyyy-MM-dd)
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTime: 数据时间起区(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/shoppedGift/pageData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
