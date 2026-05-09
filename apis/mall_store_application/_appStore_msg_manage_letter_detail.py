import os

from util.client import client

params = {
    "msgId": "",  # 消息ID
    "userId": "",  # 用户ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msg_manage_letter_detail(params=params, headers=headers):
    """
    站内信详情
    /appStore/msg/manage/letter/detail

    参数说明:
    - msgId: 消息ID
    - userId: 用户ID
    """

    url = "/appStore/msg/manage/letter/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
