import os

from util.client import client

data = {
    "id": 0,  # 公告类型ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_deleteNoticeType(data=data, headers=headers):
    """
    删除公告分类
    /mgmt/msgadmin/mgmt/msg/notice/deleteNoticeType

    参数说明:
    - id: 公告类型ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/deleteNoticeType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
