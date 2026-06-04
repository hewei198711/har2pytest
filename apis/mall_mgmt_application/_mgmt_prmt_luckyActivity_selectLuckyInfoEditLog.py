import os

from util.client import client

params = {
    "activityId": 0,  # 活动id
    "createEndTime": "",  # 编辑时间结束(yyyy-MM-dd)
    "createStartTime": "",  # 编辑时间开始(yyyy-MM-dd)
    "keyword": "",  # 搜索条件
    "modifyModule": 0,  # 修改模块(1:奖品配置；2：不中奖配置；3：奖盘配置)
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "prizeName": "",  # 奖品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_selectLuckyInfoEditLog(params=params, headers=headers):
    """
    查询活动详情编辑记录
    /mgmt/prmt/luckyActivity/selectLuckyInfoEditLog

    参数说明:
    - activityId: 活动id
    - createEndTime: 编辑时间结束(yyyy-MM-dd)
    - createStartTime: 编辑时间开始(yyyy-MM-dd)
    - keyword: 搜索条件
    - modifyModule: 修改模块(1:奖品配置；2：不中奖配置；3：奖盘配置)
    - pageNum: 当前页
    - pageSize: 每页数量
    - prizeName: 奖品名称
    """

    url = "/mgmt/prmt/luckyActivity/selectLuckyInfoEditLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
