import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "pictureCode": "",  # 图片编码
    "pictureName": "",  # 图片名称
    "pictureUrl": "",  # 图片地址
    "state": 0,  # 上下架状态：1-上架  2-下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editBoxPicture(data=data, headers=headers):
    """
    编辑盲盒海报图片
    /mgmt/prmt/luckyActivity/editBoxPicture

    参数说明:
    - id: 主键id
    - pictureCode: 图片编码
    - pictureName: 图片名称
    - pictureUrl: 图片地址
    - state: 上下架状态：1-上架  2-下架
    """

    url = "/mgmt/prmt/luckyActivity/editBoxPicture"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
