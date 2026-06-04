import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_getNoticeTypeList(headers=headers):
    """
    显示所有可见公告类型
    /mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeList
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeList"
    with client.get(url=url, headers=headers) as r:
        return r
