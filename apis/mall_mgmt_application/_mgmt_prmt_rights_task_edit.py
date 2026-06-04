import os

from util.client import client

data = {
    "amount": 0,  # 奖励金豆数量
    "cycle": 0,  # 任务周期:1-一次,2-每天,3-每周
    "endTime": "",  # 任务结束时间
    "firstLogin": False,  # 首次登录奖励:true-勾选,false-未勾选
    "firstLoginAmount": 0,  # 首次登录奖励金豆数量
    "icon": "",  # icon配置
    "id": 0,  # 主键
    "loginGiftId": 0,  # 关联登录提醒活动id
    "relation": 0,  # 关联类型:1-全部,2-指定
    "remarks": "",  # 任务描述
    "reworkType": 0,  # 任务奖励类型:1-单次奖励
    "showOrder": 0,  # 展示顺序
    "startTime": "",  # 任务开始时间
    "state": 0,  # 状态:0-草稿,1-待审核
    "taskEvent": 0,  # 任务事件:1-注册,2-登录,3-分享产品,4-分享素材,5-分享登录提醒海报
    "taskName": "",  # 任务名称
    "taskNo": "",  # 任务编号
    "taskType": 0,  # 任务类型:1-新手任务,2-日常任务,3-活动任务
    "times": 0,  # 任务次数上限
    "unlimitedTime": False,  # 是否不限时
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_task_edit(data=data, headers=headers):
    """
    编辑任务
    /mgmt/prmt/rights/task/edit

    参数说明:
    - amount: 奖励金豆数量
    - cycle: 任务周期:1-一次,2-每天,3-每周
    - endTime: 任务结束时间
    - firstLogin: 首次登录奖励:true-勾选,false-未勾选
    - firstLoginAmount: 首次登录奖励金豆数量
    - icon: icon配置
    - id: 主键
    - loginGiftId: 关联登录提醒活动id
    - relation: 关联类型:1-全部,2-指定
    - remarks: 任务描述
    - reworkType: 任务奖励类型:1-单次奖励
    - showOrder: 展示顺序
    - startTime: 任务开始时间
    - state: 状态:0-草稿,1-待审核
    - taskEvent: 任务事件:1-注册,2-登录,3-分享产品,4-分享素材,5-分享登录提醒海报
    - taskName: 任务名称
    - taskNo: 任务编号
    - taskType: 任务类型:1-新手任务,2-日常任务,3-活动任务
    - times: 任务次数上限
    - unlimitedTime: 是否不限时
    """

    url = "/mgmt/prmt/rights/task/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
