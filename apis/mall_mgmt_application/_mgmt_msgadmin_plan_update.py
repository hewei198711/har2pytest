import os

from util.client import client

data = {
    "content": "",  # 发送内容
    "contentFrom": 0,  # 模板来源  0 自由编辑, 1 消息模版
    "cronDisPlay": "",  # 定时回显字段
    "cronVo": {"cronSelect": 0, "day": "", "hour": "", "minutes": "", "month": ""},  # 定时发送内容参数
    "endTime": "",  # 发送时间范围-结束时间 17:00
    "id": 0,  # 主键Id
    "msgTitle": "",  # 消息标题
    "msgType": 0,  # 消息类型
    "operatorId": "",  # 操作者ID
    "operatorName": "",  # 操作者名称
    "params": "",  # 需要替代的参数
    "sceneDesc": "",  # 发送场景描述
    "sendLetter": 0,  # 是否需要发送站内信,0:否,1:是
    "sendSms": 0,  # 是否需要发送站短信,0:否,1:是
    "startTime": "",  # 发送时间范围-开始时间 08:00
    "status": 0,  # 状态 1可用 0不可用
    "templateCode": "",  # 模板code
    "templateName": "",  # 模板名称
    "templateTitle": "",  # 模板标题
    "triggerType": 0,  # 触发类型 0 即时触发 1 定时触发
    "updateTime": "",  # 更新时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_plan_update(data=data, headers=headers):
    """
    更新单个发送计划（系统消息）接口
    /mgmt/msgadmin/plan/update

    参数说明:
    - content: 发送内容
    - contentFrom: 模板来源  0 自由编辑, 1 消息模版
    - cronDisPlay: 定时回显字段
    - cronVo: 定时发送内容参数
    - cronVo.cronSelect: 定时任务选择类型 1每年 2每月 3每天
    - cronVo.day: 天
    - cronVo.hour: 时
    - cronVo.minutes: 分
    - cronVo.month: 月
    - endTime: 发送时间范围-结束时间 17:00
    - id: 主键Id
    - msgTitle: 消息标题
    - msgType: 消息类型
    - operatorId: 操作者ID
    - operatorName: 操作者名称
    - params: 需要替代的参数
    - sceneDesc: 发送场景描述
    - sendLetter: 是否需要发送站内信,0:否,1:是
    - sendSms: 是否需要发送站短信,0:否,1:是
    - startTime: 发送时间范围-开始时间 08:00
    - status: 状态 1可用 0不可用
    - templateCode: 模板code
    - templateName: 模板名称
    - templateTitle: 模板标题
    - triggerType: 触发类型 0 即时触发 1 定时触发
    - updateTime: 更新时间
    """

    url = "/mgmt/msgadmin/plan/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
