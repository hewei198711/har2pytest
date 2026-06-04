import os

from util.client import client

data = {
    "attachmentName": "",  # 附件名称
    "attachmentUrl": "",  # 附件地址
    "content": "",  # 内容
    "releaseTime": "",  # 发布时间（定时触发时才有）
    "saveAsDraft": 0,  # 是否保存为草稿：0->否；1->是
    "showMall": 0,  # 是否在商城展示：0->否；1->是
    "showStore": 0,  # 是否在服务中心展示：0->否；1->是
    "title": "",  # 公告标题
    "triggerType": 0,  # 触发类型：0->即时触发；1->定时触发
    "typeId": 0,  # 公告类型ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_addNotice(data=data, headers=headers):
    """
    添加公告
    /mgmt/msgadmin/mgmt/msg/notice/addNotice

    参数说明:
    - attachmentName: 附件名称
    - attachmentUrl: 附件地址
    - content: 内容
    - releaseTime: 发布时间（定时触发时才有）
    - saveAsDraft: 是否保存为草稿：0->否；1->是
    - showMall: 是否在商城展示：0->否；1->是
    - showStore: 是否在服务中心展示：0->否；1->是
    - title: 公告标题
    - triggerType: 触发类型：0->即时触发；1->定时触发
    - typeId: 公告类型ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/addNotice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
