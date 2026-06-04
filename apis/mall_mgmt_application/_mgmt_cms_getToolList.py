import os

from util.client import client

data = {
    "category": 0,  # 分类，1:我的账户, 2:代购代办, 3:业务大厅, 4:我的工具
    "location": 0,  # 显示位置，1：PC商城首页，2：APP，3：小程序
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getToolList(data=data, headers=headers):
    """
    获取工具列表
    /mgmt/cms/getToolList

    参数说明:
    - category: 分类，1:我的账户, 2:代购代办, 3:业务大厅, 4:我的工具
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/getToolList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
