import os

from util.client import client

data = {
    "platformType": 0,  # 平台类型：1商城 2服务中心
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msgadmin_msg_notice_readAll(data=data, headers=headers):
    """
    全部已读
    /appStore/msgadmin/msg/notice/readAll

    参数说明:
    - platformType: 平台类型：1商城 2服务中心
    """

    url = "/appStore/msgadmin/msg/notice/readAll"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
