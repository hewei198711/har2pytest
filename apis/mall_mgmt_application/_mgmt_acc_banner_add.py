import os

from util.client import client

data = {
    "bannerName": "",  # 名称
    "bannerShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
    "id": 0,  # ID
    "imageUrl": "",  # 图片地址
    "linkUrl": "",  # banner图链接地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_banner_add(data=data, headers=headers):
    """
    添加轮播图
    /mgmt/acc/banner/add

    参数说明:
    - bannerName: 名称
    - bannerShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - id: ID
    - imageUrl: 图片地址
    - linkUrl: banner图链接地址
    """

    url = "/mgmt/acc/banner/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
