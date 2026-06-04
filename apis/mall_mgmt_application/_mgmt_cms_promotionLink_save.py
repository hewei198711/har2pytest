import os

from util.client import client

data = {
    "jumpPath": "",  # 跳转路径
    "platform": 0,  # 平台: 1.APP 2.小程序
    "thirdPartySoftwareName": "",  # 第三方软件名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promotionLink_save(data=data, headers=headers):
    """
    新建第三方软件推广链接
    /mgmt/cms/promotionLink/save

    参数说明:
    - jumpPath: 跳转路径
    - platform: 平台: 1.APP 2.小程序
    - thirdPartySoftwareName: 第三方软件名称
    """

    url = "/mgmt/cms/promotionLink/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
