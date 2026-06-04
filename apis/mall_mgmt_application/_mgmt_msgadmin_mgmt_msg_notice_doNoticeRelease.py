import os

from util.client import client

data = {
    "id": 0,  # 公告ID
    "type": 0,  # 操作类型：1->发布；2->撤销发布
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_doNoticeRelease(data=data, headers=headers):
    """
    执行公告发布与撤销
    /mgmt/msgadmin/mgmt/msg/notice/doNoticeRelease

    参数说明:
    - id: 公告ID
    - type: 操作类型：1->发布；2->撤销发布
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/doNoticeRelease"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
