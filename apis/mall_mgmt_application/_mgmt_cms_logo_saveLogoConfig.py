import os

from util.client import client

data = {
    "imageUrl": "",  # logo图片
    "logoName": "",  # 商城logo名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_logo_saveLogoConfig(data=data, headers=headers):
    """
    保存logo配置
    /mgmt/cms/logo/saveLogoConfig

    参数说明:
    - imageUrl: logo图片
    - logoName: 商城logo名称
    """

    url = "/mgmt/cms/logo/saveLogoConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
