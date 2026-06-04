import os

from util.client import client

data = {
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用
    "isDefault": 0,  # 是否默认: 0.否 1.是
    "memberTypes": "",  # 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    "sort": 0,  # 排序
    "url": "",  # 链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_saveBackgroundStyle(data=data, headers=headers):
    """
    保存背景样式信息
    /mgmt/cms/backgroundStyle/saveBackgroundStyle

    参数说明:
    - enableStatus: 启用状态: 0.禁用 1.启用
    - isDefault: 是否默认: 0.否 1.是
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    - url: 链接
    """

    url = "/mgmt/cms/backgroundStyle/saveBackgroundStyle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
