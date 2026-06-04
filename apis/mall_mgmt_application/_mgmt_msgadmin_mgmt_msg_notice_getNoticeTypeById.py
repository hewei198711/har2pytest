import os

from util.client import client

params = {
    "id": "",  # 公告分类ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_getNoticeTypeById(params=params, headers=headers):
    """
    根据公告分类ID获取公告分类
    /mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeById

    参数说明:
    - id: 公告分类ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
