import os

from util.client import client

params = {
    "activityName": "",  # 活动名称
    "createTimeEnd": "",  # 创建时间止区
    "createTimeStart": "",  # 创建时间起区
    "endTime": "",  # 活动结束时间
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platforms": [],  # 领券平台:1-APP,2-PC,4-小程序
    "selectedIds": [],  # 选中记录id
    "startTime": "",  # 活动开始时间
    "status": 0,  # 状态:1-待审核,2-进行中,3-已完成,4-已驳回,5-草稿,6-已停止,7-待开始
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_loginGift(params=params, headers=headers):
    """
    登录有礼活动各状态数量
    /mgmt/prmt/state/loginGift

    参数说明:
    - activityName: 活动名称
    - createTimeEnd: 创建时间止区
    - createTimeStart: 创建时间起区
    - endTime: 活动结束时间
    - pageNum: 当前页
    - pageSize: 每页数量
    - platforms: 领券平台:1-APP,2-PC,4-小程序
    - selectedIds: 选中记录id
    - startTime: 活动开始时间
    - status: 状态:1-待审核,2-进行中,3-已完成,4-已驳回,5-草稿,6-已停止,7-待开始
    """

    url = "/mgmt/prmt/state/loginGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
