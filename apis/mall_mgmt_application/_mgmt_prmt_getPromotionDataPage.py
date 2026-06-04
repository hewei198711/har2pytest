import os

from util.client import client

params = {
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "promotionId": 0,  # 活动id
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getPromotionDataPage(params=params, headers=headers):
    """
    分页获取活动数据
    /mgmt/prmt/getPromotionDataPage

    参数说明:
    - endTime: 结束时间
    - pageNum: 当前页
    - pageSize: 每页条数
    - promotionId: 活动id
    - startTime: 开始时间
    """

    url = "/mgmt/prmt/getPromotionDataPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
