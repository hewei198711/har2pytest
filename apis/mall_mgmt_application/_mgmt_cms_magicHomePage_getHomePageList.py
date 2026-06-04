import os

from util.client import client

data = {
    "createTimeEnd": "",  # 创建时间结束
    "createTimeStart": "",  # 创建时间开始
    "homePageStatus": 0,  # 首页状态: -1:审核不通过 0:未发布; 1:待审核; 2:定时发布; 3:已发布
    "isRecycle": 0,  # 是否查询回收站 1.是 0.否
    "location": 0,  # 端口(显示位置): 2:APP; 3:小程序
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_getHomePageList(data=data, headers=headers):
    """
    获取魔法首页列表
    /mgmt/cms/magicHomePage/getHomePageList

    参数说明:
    - createTimeEnd: 创建时间结束
    - createTimeStart: 创建时间开始
    - homePageStatus: 首页状态: -1:审核不通过 0:未发布; 1:待审核; 2:定时发布; 3:已发布
    - isRecycle: 是否查询回收站 1.是 0.否
    - location: 端口(显示位置): 2:APP; 3:小程序
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/magicHomePage/getHomePageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
