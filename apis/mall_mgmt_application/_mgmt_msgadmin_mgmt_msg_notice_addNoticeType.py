import os

from util.client import client

data = {
    "typeDesc": "",  # 描述
    "typeName": "",  # 类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_addNoticeType(data=data, headers=headers):
    """
    添加公告分类
    /mgmt/msgadmin/mgmt/msg/notice/addNoticeType

    参数说明:
    - typeDesc: 描述
    - typeName: 类型名称
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/addNoticeType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
