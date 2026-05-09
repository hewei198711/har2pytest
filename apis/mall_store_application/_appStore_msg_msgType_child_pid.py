import os

from util.client import client

params = {
    "pid": "",  # pid
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msg_msgType_child_pid(params=params, headers=headers):
    """
    查询子节点消息类型内容,仅查询有效
    /appStore/msg/msgType/child/{pid}

    参数说明:
    - pid: pid
    """

    url = f"/appStore/msg/msgType/child/{params['pid']}"
    with client.get(url=url, headers=headers) as r:
        return r
