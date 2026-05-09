import os

from util.client import client

params = {
    "platformType": "",  # 平台类型：1商城 2服务中心
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msgadmin_msg_notice_getToppingNotice(params=params, headers=headers):
    """
    获取置顶公告
    /appStore/msgadmin/msg/notice/getToppingNotice

    参数说明:
    - platformType: 平台类型：1商城 2服务中心
    """

    url = "/appStore/msgadmin/msg/notice/getToppingNotice"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
