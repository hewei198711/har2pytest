import os

from util.client import client

data = {
    "bannerUrl": "",  # banner图片/分享海报的banner图片
    "id": 0,  # 主键
    "logoUrl": "",  # 分享海报的logo图片
    "tittleName": "",  # 分享海报标题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_updatePhotoById(data=data, headers=headers):
    """
    更新banner图片/分享海报
    /mgmt/miniapp/updatePhotoById

    参数说明:
    - bannerUrl: banner图片/分享海报的banner图片
    - id: 主键
    - logoUrl: 分享海报的logo图片
    - tittleName: 分享海报标题
    """

    url = "/mgmt/miniapp/updatePhotoById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
