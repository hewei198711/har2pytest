import os

from util.client import client

data = {
    "id": 0,  # 自增主键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msgadmin_msg_notice_getNoticeDetail(data=data, headers=headers):
    """
    获取公告详情
    /appStore/msgadmin/msg/notice/getNoticeDetail

    参数说明:
    - id: 自增主键
    """

    url = "/appStore/msgadmin/msg/notice/getNoticeDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
