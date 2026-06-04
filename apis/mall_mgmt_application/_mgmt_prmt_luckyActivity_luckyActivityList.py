import os

from util.client import client

params = {
    "activityCode": "",  # 活动编号
    "activityName": "",  # 活动名称
    "createEndTime": "",  # 创建时间结束(yyyy-MM-dd)
    "createStartTime": "",  # 创建时间开始(yyyy-MM-dd)
    "endTimeEnd": "",  # 活动结束时间,结束(yyyy-MM-dd)
    "endTimeStart": "",  # 活动结束时间,开始(yyyy-MM-dd)
    "keyword": "",  # 搜索条件
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTimeEnd": "",  # 活动开始时间,结束(yyyy-MM-dd)
    "startTimeStart": "",  # 活动开始时间,开始(yyyy-MM-dd)
    "state": 0,  # 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
    "states": [],  # 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_luckyActivityList(params=params, headers=headers):
    """
    抽奖活动管理列表
    /mgmt/prmt/luckyActivity/luckyActivityList

    参数说明:
    - activityCode: 活动编号
    - activityName: 活动名称
    - createEndTime: 创建时间结束(yyyy-MM-dd)
    - createStartTime: 创建时间开始(yyyy-MM-dd)
    - endTimeEnd: 活动结束时间,结束(yyyy-MM-dd)
    - endTimeStart: 活动结束时间,开始(yyyy-MM-dd)
    - keyword: 搜索条件
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTimeEnd: 活动开始时间,结束(yyyy-MM-dd)
    - startTimeStart: 活动开始时间,开始(yyyy-MM-dd)
    - state: 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
    - states: 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
    """

    url = "/mgmt/prmt/luckyActivity/luckyActivityList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
