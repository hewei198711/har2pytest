import os

from util.client import client

data = {
    "avatarUrl": "",  # 头像图片链接
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用
    "memberTypes": "",  # 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_saveAvatar(data=data, headers=headers):
    """
    保存头像图片
    /mgmt/cms/avatar/saveAvatar

    参数说明:
    - avatarUrl: 头像图片链接
    - enableStatus: 启用状态: 0.禁用 1.启用
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    """

    url = "/mgmt/cms/avatar/saveAvatar"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
