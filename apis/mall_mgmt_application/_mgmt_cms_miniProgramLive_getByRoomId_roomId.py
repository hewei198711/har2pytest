import os

from util.client import client

params = {
    "roomId": 0,  # roomId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_miniProgramLive_getByRoomId_roomId(params=params, headers=headers):
    """
    获取直播间信息
    /mgmt/cms/miniProgramLive/getByRoomId/{roomId}

    参数说明:
    - roomId: roomId
    """

    url = f"/mgmt/cms/miniProgramLive/getByRoomId/{params['roomId']}"
    with client.get(url=url, headers=headers) as r:
        return r
