import os

from util.client import client

params = {
    "avatarId": 0,  # avatarId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_editAvatar_avatarId(params=params, headers=headers):
    """
    修改头像图片
    /mgmt/cms/avatar/editAvatar/{avatarId}

    参数说明:
    - avatarId: avatarId
    - avatarUrl: 头像图片链接
    - enableStatus: 启用状态: 0.禁用 1.启用
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    """

    url = f"/mgmt/cms/avatar/editAvatar/{params['avatarId']}"
    with client.get(url=url, headers=headers) as r:
        return r
