import os

from util.client import client

params = {
    "endTime": "",  # 发布时间
    "msgTitle": "",  # 消息标题
    "msgType": 0,  # 消息类型
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "planSceneId": 0,  # 业务主题主键Id
    "planStatus": 0,  # 发布状态 0 待审核, 1 通过  ,2 已驳回 , 3 撤销发送
    "receiverType": 0,  # 渠道
    "startTime": "",  # 发布时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_list(params=params, headers=headers):
    """
    手工消息列表
    /mgmt/msgadmin/handmade/list

    参数说明:
    - endTime: 发布时间
    - msgTitle: 消息标题
    - msgType: 消息类型
    - planSceneId: 业务主题主键Id
    - planStatus: 发布状态 0 待审核, 1 通过  ,2 已驳回 , 3 撤销发送
    - receiverType: 渠道
    - startTime: 发布时间
    """

    url = "/mgmt/msgadmin/handmade/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
