import os

from util.client import client

data = {
    "id": 0,  # 自增主键
    "typeDesc": "",  # 描述
    "typeName": "",  # 类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_editNoticeType(data=data, headers=headers):
    """
    编辑公告分类
    /mgmt/msgadmin/mgmt/msg/notice/editNoticeType

    参数说明:
    - id: 自增主键
    - typeDesc: 描述
    - typeName: 类型名称
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/editNoticeType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
