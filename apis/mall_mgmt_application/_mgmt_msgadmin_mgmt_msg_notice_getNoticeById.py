import os

from util.client import client

params = {
    "id": "",  # 公告ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_getNoticeById(params=params, headers=headers):
    """
    根据公告ID获取公告
    /mgmt/msgadmin/mgmt/msg/notice/getNoticeById

    参数说明:
    - id: 公告ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/getNoticeById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
