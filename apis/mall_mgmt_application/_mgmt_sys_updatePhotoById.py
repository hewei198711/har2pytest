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


def _mgmt_sys_updatePhotoById(data=data, headers=headers):
    """
    通过主键更改图片
    /mgmt/sys/updatePhotoById

    参数说明:
    - bannerUrl: banner图片/分享海报的banner图片
    - id: 主键
    - logoUrl: 分享海报的logo图片
    - tittleName: 分享海报标题
    """

    url = "/mgmt/sys/updatePhotoById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
