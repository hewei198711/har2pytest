import os

from util.client import client

data = {
    "displayType": 0,  # 查看类型 1:按顾客身份查看; 2:按用户展示名单
    "displayUserSerial": "",  # 展示用户关联序列号
    "memberTypes": [],  # 按顾客身份查看: 1.会员; 2.VIP会员; 3.云商; 4.微店;
    "roomId": 0,  # 直播间id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_miniProgramLive_edit(data=data, headers=headers):
    """
    编辑直播间信息
    /mgmt/cms/miniProgramLive/edit

    参数说明:
    - displayType: 查看类型 1:按顾客身份查看; 2:按用户展示名单
    - displayUserSerial: 展示用户关联序列号
    - memberTypes: 按顾客身份查看: 1.会员; 2.VIP会员; 3.云商; 4.微店;
    - roomId: 直播间id
    """

    url = "/mgmt/cms/miniProgramLive/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
