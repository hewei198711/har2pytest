import os

from util.client import client

data = {
    "id": 0,  # 自增主键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_changeNoticeTypeStatusById(data=data, headers=headers):
    """
    根据公告ID更改公告类型状态，原来显示则变成隐藏，原来隐藏则变成显示
    /mgmt/msgadmin/mgmt/msg/notice/changeNoticeTypeStatusById

    参数说明:
    - id: 自增主键
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/changeNoticeTypeStatusById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
