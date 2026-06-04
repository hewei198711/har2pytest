import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_editAvatarFrame_id(params=params, headers=headers):
    """
    修改头像框图片信息
    /mgmt/cms/avatarFrame/editAvatarFrame/{id}

    参数说明:
    - id: id
    - avatarFrameUrl: 头像框图片链接
    - displayType: 查看类型 1:按顾客身份查看; 2:按用户展示名单
    - displayUserSerial: 展示用户关联序列号
    - enableStatus: 启用状态: 0.禁用 1.启用
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    """

    url = f"/mgmt/cms/avatarFrame/editAvatarFrame/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
