import os

from util.client import client

data = {
    "content": "",  # 消息内容
    "endTime": "",  # 结束时间
    "msgType": 0,  # 消息类型
    "msgTypeList": [],  # TODO: 添加参数说明
    "pageNum": 0,  # 分页查询起始位置
    "pageSize": 0,  # 每页查询记录数
    "senderId": "",  # 发布人ID
    "senderName": "",  # 发布人
    "startTime": "",  # 开始时间
    "status": 0,  # 消息状态，0：未读；1：已读
    "statusList": [],  # TODO: 添加参数说明
    "systemId": 0,  # 请求服务ID
    "userId": "",  # 当前登录人
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msg_api_letterMsg_queryLetterMsgGroupStatus(data=data, headers=headers):
    """
    消息列表查询(未读排前)
    /appStore/msg/api/letterMsg/queryLetterMsgGroupStatus

    参数说明:
    - content: 消息内容
    - endTime: 结束时间
    - msgType: 消息类型
    - pageNum: 分页查询起始位置
    - pageSize: 每页查询记录数
    - senderId: 发布人ID
    - senderName: 发布人
    - startTime: 开始时间
    - status: 消息状态，0：未读；1：已读
    - systemId: 请求服务ID
    - userId: 当前登录人
    """

    url = "/appStore/msg/api/letterMsg/queryLetterMsgGroupStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
