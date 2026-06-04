import os

from util.client import client

params = {
    "id": 0,  # id
    "sceneId": 0,  # sceneId
    "status": 0,  # status
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_msgadmin_plan_updateStatus_id_sceneId_status(params=params, headers=headers):
    """
    更新单个发送计划（系统消息）状态接口
    /mgmt/msgadmin/plan/updateStatus/{id}/{sceneId}/{status}

    参数说明:
    - id: id
    - sceneId: sceneId
    - status: status
    """

    url = f"/mgmt/msgadmin/plan/updateStatus/{params['id']}/{params['sceneId']}/{params['status']}"
    with client.get(url=url, headers=headers) as r:
        return r
