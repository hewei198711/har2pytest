import os

from util.client import client

data = {
    "category": 0,  # 内容分类，1：分享好友内容配置，2：保存图像内容配置，3：订单分享内容配置
    "imageList": [],  # 图片列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_dkxp_shareContent_saveImageList(data=data, headers=headers):
    """
    新增内容图片(多张)
    /mgmt/cms/dkxp/shareContent/saveImageList

    参数说明:
    - category: 内容分类，1：分享好友内容配置，2：保存图像内容配置，3：订单分享内容配置
    - imageList: 图片列表
    """

    url = "/mgmt/cms/dkxp/shareContent/saveImageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
