import os

from util.client import client

params = {
    "endTime": "",  # 创建时间止区(yyyy-MM-dd)
    "ids": [],  # 勾选的id列表
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "startTime": "",  # 创建时间起区(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_gift_pageGiftMain(params=params, headers=headers):
    """
    分页查询赠品派发任务
    /mgmt/prmt/gift/pageGiftMain

    参数说明:
    - endTime: 创建时间止区(yyyy-MM-dd)
    - ids: 勾选的id列表
    - pageNum: 当前页
    - pageSize: 每页条数
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - startTime: 创建时间起区(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/gift/pageGiftMain"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
