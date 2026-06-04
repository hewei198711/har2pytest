import os

from util.client import client

data = {
    "channel": 0,  # 平台筛选：0->所有平台; 1->商城; 2->服务中心后台;不传为默认0
    "createBeginTime": "",  # 创建起始时间
    "createEndTime": "",  # 创建结束时间
    "pageNum": 0,  # 页数,默认为1
    "pageSize": 0,  # 每页显示数，默认为10
    "releaseBeginTime": "",  # 发布起始时间
    "releaseEndTime": "",  # 发布结束时间
    "showType": 0,  # 显示方式：-3->草稿，-2->待审核，-1->待发布，0->已发布，1->已驳回，2->已取消;不传为默认全部
    "title": "",  # 公告标题
    "typeId": 0,  # 公告类型ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_getNoticeByPage(data=data, headers=headers):
    """
    获取公告分页列表
    /mgmt/msgadmin/mgmt/msg/notice/getNoticeByPage

    参数说明:
    - channel: 平台筛选：0->所有平台; 1->商城; 2->服务中心后台;不传为默认0
    - createBeginTime: 创建起始时间
    - createEndTime: 创建结束时间
    - pageNum: 页数,默认为1
    - pageSize: 每页显示数，默认为10
    - releaseBeginTime: 发布起始时间
    - releaseEndTime: 发布结束时间
    - showType: 显示方式：-3->草稿，-2->待审核，-1->待发布，0->已发布，1->已驳回，2->已取消;不传为默认全部
    - title: 公告标题
    - typeId: 公告类型ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/getNoticeByPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
