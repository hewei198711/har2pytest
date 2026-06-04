import os

from util.client import client

data = {
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用 传null则为全部
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_getAvatarFrameList(data=data, headers=headers):
    """
    头像框图片列表
    /mgmt/cms/avatarFrame/getAvatarFrameList

    参数说明:
    - enableStatus: 启用状态: 0.禁用 1.启用 传null则为全部
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/avatarFrame/getAvatarFrameList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
