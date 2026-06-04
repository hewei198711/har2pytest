import os

from util.client import client

params = {
    "toolId": 0,  # toolId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_editTool_toolId(params=params, headers=headers):
    """
    编辑工具
    /mgmt/cms/editTool/{toolId}

    参数说明:
    - categoryId: icon对应的分类id(APP、小程序)
    - iconName: 1:3模式菜单图标名称
    - iconNameOf85: 85%模式菜单图标名称
    - iconUrl: icon图标链接
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    - sort: 排序
    - status: 状态 1.启用 0.禁用
    - titleId: PC商城对应的类型标题id
    - toolId: toolId
    """

    url = f"/mgmt/cms/editTool/{params['toolId']}"
    with client.get(url=url, headers=headers) as r:
        return r
