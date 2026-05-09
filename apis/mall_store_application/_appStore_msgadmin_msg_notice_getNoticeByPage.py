import os

from util.client import client

data = {
    "keywords": "",  # 关键词
    "pageNum": 0,  # 页数,默认为1
    "pageSize": 0,  # 每页显示数，默认为10
    "platformType": 0,  # 平台类型：0全部 1商城 2服务中心
    "readFlag": 0,  # 读取状态，1已读取，0未读取
    "releaseTimeEnd": "",  # 发布结束时间 格式YYYY-MM-DD
    "releaseTimeStart": "",  # 发布开始时间 格式YYYY-MM-DD
    "returnContent": False,  # 是否返回内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msgadmin_msg_notice_getNoticeByPage(data=data, headers=headers):
    """
    获取公告分页列表
    /appStore/msgadmin/msg/notice/getNoticeByPage

    参数说明:
    - keywords: 关键词
    - pageNum: 页数,默认为1
    - pageSize: 每页显示数，默认为10
    - platformType: 平台类型：0全部 1商城 2服务中心
    - readFlag: 读取状态，1已读取，0未读取
    - releaseTimeEnd: 发布结束时间 格式YYYY-MM-DD
    - releaseTimeStart: 发布开始时间 格式YYYY-MM-DD
    - returnContent: 是否返回内容
    """

    url = "/appStore/msgadmin/msg/notice/getNoticeByPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
