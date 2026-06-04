import os

from util.client import client

data = {
    "category": 0,  # 内容分类，1：分享好友内容配置，2：保存图像内容配置
    "imageUrl": "",  # 文案图片链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_dkxp_shareContent_saveImage(data=data, headers=headers):
    """
    新增内容图片
    /mgmt/cms/dkxp/shareContent/saveImage

    参数说明:
    - category: 内容分类，1：分享好友内容配置，2：保存图像内容配置
    - imageUrl: 文案图片链接
    """

    url = "/mgmt/cms/dkxp/shareContent/saveImage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
