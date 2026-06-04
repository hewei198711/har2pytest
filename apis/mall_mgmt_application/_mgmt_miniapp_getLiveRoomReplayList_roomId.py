import os

from util.client import client

params = {
    "roomId": 0,  # 直播间id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_miniapp_getLiveRoomReplayList_roomId(params=params, headers=headers):
    """
    获取直播间回放列表数据
    /mgmt/miniapp/getLiveRoomReplayList/{roomId}

    参数说明:
    - roomId: 直播间id
    """

    url = f"/mgmt/miniapp/getLiveRoomReplayList/{params['roomId']}"
    with client.get(url=url, headers=headers) as r:
        return r
