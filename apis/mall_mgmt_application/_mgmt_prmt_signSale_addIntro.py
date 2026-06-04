import os

from util.client import client

data = {
    "agreement": "",  # 自动扣款协议
    "introMobile": "",  # 活动介绍图移动端
    "introPc": "",  # 活动介绍图PC端
    "rule": "",  # 活动规则
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_addIntro(data=data, headers=headers):
    """
    新建签约购活动介绍
    /mgmt/prmt/signSale/addIntro

    参数说明:
    - agreement: 自动扣款协议
    - introMobile: 活动介绍图移动端
    - introPc: 活动介绍图PC端
    - rule: 活动规则
    """

    url = "/mgmt/prmt/signSale/addIntro"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
