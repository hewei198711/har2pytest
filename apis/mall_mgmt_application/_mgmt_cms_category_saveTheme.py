import os

from util.client import client

data = {
    "content": [{"icon": "", "id": 0, "title": ""}],  # 分类内容
    "id": "",  # 主题id, 新增不传，编辑传
    "isDefault": 0,  # 是否默认（0：是系统默认，1：非系统默认）
    "location": 0,  # 显示位置 （1：PC, 2: APP，3：小程序）
    "name": "",  # 主题名称
    "shelfConfig": 0,  # 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    "shelfOffTime": 0,  # 下架时间
    "shelfUpTime": 0,  # 上架时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_category_saveTheme(data=data, headers=headers):
    """
    新增主题
    /mgmt/cms/category/saveTheme

    参数说明:
    - content: 分类内容
    - content.icon: 图标地址
    - content.id: 分类id
    - content.title: 分类名称
    - id: 主题id, 新增不传，编辑传
    - isDefault: 是否默认（0：是系统默认，1：非系统默认）
    - location: 显示位置 （1：PC, 2: APP，3：小程序）
    - name: 主题名称
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    - shelfOffTime: 下架时间
    - shelfUpTime: 上架时间
    """

    url = "/mgmt/cms/category/saveTheme"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
