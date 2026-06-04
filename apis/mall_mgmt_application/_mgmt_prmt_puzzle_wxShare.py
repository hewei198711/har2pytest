import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "wxSharePicture": "",  # 小程序分享卡片图片地址
    "wxShareRemark": "",  # 小程序分享卡片文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_wxShare(data=data, headers=headers):
    """
    修改小程序分享卡片配置
    /mgmt/prmt/puzzle/wxShare

    参数说明:
    - id: 活动id
    - wxSharePicture: 小程序分享卡片图片地址
    - wxShareRemark: 小程序分享卡片文案
    """

    url = "/mgmt/prmt/puzzle/wxShare"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
