import os

from util.client import client

data = {
    "operatorId": 0,  # 操作者ID
    "operatorName": "",  # 操作者名称
    "planSceneId": 0,  # TODO: 添加参数说明
    "receiverShowStatus": 0,  # 名单展示状态: 0:隐藏; 1:展示 ; 2:周期展示
    "showEndTime": "",  # 周期展示,结束时间
    "status": 0,  # 状态 (1可用,0不可用)
    "title": "",  # 业务主题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_planSceneTheme_disable(data=data, headers=headers):
    """
    禁用
    /mgmt/msgadmin/planSceneTheme/disable

    参数说明:
    - operatorId: 操作者ID
    - operatorName: 操作者名称
    - receiverShowStatus: 名单展示状态: 0:隐藏; 1:展示 ; 2:周期展示
    - showEndTime: 周期展示,结束时间
    - status: 状态 (1可用,0不可用)
    - title: 业务主题
    """

    url = "/mgmt/msgadmin/planSceneTheme/disable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
