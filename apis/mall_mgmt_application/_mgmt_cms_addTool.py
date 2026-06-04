import os

from util.client import client

data = {
    "categoryId": 0,  # icon对应的分类id(APP、小程序)
    "iconName": "",  # 1:3模式菜单图标名称
    "iconNameOf85": "",  # 85%模式菜单图标名称
    "iconUrl": "",  # icon图标链接
    "location": 0,  # 显示位置，1：PC商城首页，2：APP，3：小程序
    "sort": 0,  # 排序
    "status": 0,  # 状态 1.启用 0.禁用
    "titleId": 0,  # PC商城对应的类型标题id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_addTool(data=data, headers=headers):
    """
    添加新工具
    /mgmt/cms/addTool

    参数说明:
    - categoryId: icon对应的分类id(APP、小程序)
    - iconName: 1:3模式菜单图标名称
    - iconNameOf85: 85%模式菜单图标名称
    - iconUrl: icon图标链接
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    - sort: 排序
    - status: 状态 1.启用 0.禁用
    - titleId: PC商城对应的类型标题id
    """

    url = "/mgmt/cms/addTool"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
