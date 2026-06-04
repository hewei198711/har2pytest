import os

from util.client import client

params = {
    "pageNum": "",  # 当前页
    "pageSize": "",  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_getNoticeTypeByPage(params=params, headers=headers):
    """
    分页获取公告类型列表
    /mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeByPage

    参数说明:
    - pageNum: 当前页
    - pageSize: 每页显示数
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/getNoticeTypeByPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
