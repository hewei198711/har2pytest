import os

from util.client import client

data = {
    "avatarFrameUrl": "",  # 头像框图片链接
    "displayType": 0,  # 查看类型 1:按顾客身份查看; 2:按用户展示名单
    "displayUserSerial": "",  # 展示用户关联序列号
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用
    "memberTypes": "",  # 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_saveAvatarFrame(data=data, headers=headers):
    """
    保存头像框图片信息
    /mgmt/cms/avatarFrame/saveAvatarFrame

    参数说明:
    - avatarFrameUrl: 头像框图片链接
    - displayType: 查看类型 1:按顾客身份查看; 2:按用户展示名单
    - displayUserSerial: 展示用户关联序列号
    - enableStatus: 启用状态: 0.禁用 1.启用
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    """

    url = "/mgmt/cms/avatarFrame/saveAvatarFrame"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
