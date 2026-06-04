import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "introMobile": "",  # 移动端活动介绍(富文本)
    "introPc": "",  # PC端活动介绍(富文本)
    "pcPicture": "",  # PC端活动主图地址
    "picture": "",  # 移动端活动主图地址
    "promotionName": "",  # 活动名称
    "sharePicture": "",  # 活动分享海报地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_editOtherInfo(data=data, headers=headers):
    """
    修改其它信息
    /mgmt/prmt/combine/editOtherInfo

    参数说明:
    - id: 活动id
    - introMobile: 移动端活动介绍(富文本)
    - introPc: PC端活动介绍(富文本)
    - pcPicture: PC端活动主图地址
    - picture: 移动端活动主图地址
    - promotionName: 活动名称
    - sharePicture: 活动分享海报地址
    """

    url = "/mgmt/prmt/combine/editOtherInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
