import os

from util.client import client

data = {
    "id": 0,  # 公告ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_deleteNotice(data=data, headers=headers):
    """
    删除公告
    /mgmt/msgadmin/mgmt/msg/notice/deleteNotice

    参数说明:
    - id: 公告ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/deleteNotice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
