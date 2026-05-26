import os

from util.client import client

data = {
    "pictureCode": "tt051903",  # 图片编码
    "pictureName": "盲盒海报三号",  # 图片名称
    "pictureUrl": "https://ucoss-test.perfect99.com/mall-center-promotion/20260519160337TCNtl.png",  # 图片地址
    "state": 1,  # 上下架状态：1-上架  2-下架
    "id": None,  # 主键id
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_luckyActivity_addBoxPicture(data=data, headers=headers):
    """
    新增盲盒海报图片
    /mgmt/prmt/luckyActivity/addBoxPicture

    参数说明:
    - id: 主键id
    - pictureCode: 图片编码
    - pictureName: 图片名称
    - pictureUrl: 图片地址
    - state: 上下架状态：1-上架  2-下架
    """

    url = "/mgmt/prmt/luckyActivity/addBoxPicture"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
