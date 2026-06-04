import os

from util.client import client

data = {
    "introMobilePicture": "",  # 活动介绍图移动端
    "introPcPicture": "",  # 活动介绍图PC端
    "rule": "",  # 活动规则
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_libertySale_addIntro(data=data, headers=headers):
    """
    新增随心购活动介绍
    /mgmt/prmt/libertySale/addIntro

    参数说明:
    - introMobilePicture: 活动介绍图移动端
    - introPcPicture: 活动介绍图PC端
    - rule: 活动规则
    """

    url = "/mgmt/prmt/libertySale/addIntro"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
