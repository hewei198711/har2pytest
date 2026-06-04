import os

from util.client import client

data = {
    "bannedStatus": 0,  # 直播间禁用状态: 0:启用  1:禁用
    "roomId": 0,  # 直播间ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_updateLiveRoomStatus(data=data, headers=headers):
    """
    修改直播间启用/禁用状态
    /mgmt/miniapp/updateLiveRoomStatus

    参数说明:
    - bannedStatus: 直播间禁用状态: 0:启用  1:禁用
    - roomId: 直播间ID
    """

    url = "/mgmt/miniapp/updateLiveRoomStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
