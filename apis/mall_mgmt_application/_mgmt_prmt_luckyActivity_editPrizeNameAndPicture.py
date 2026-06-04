import os

from util.client import client

data = {
    "modifyModule": 0,  # 修改模块类型(4-中奖名称，5-中奖图片)
    "prizeId": 0,  # 奖品id
    "prizeName": "",  # 奖品名称
    "prizePicture": "",  # 奖品图片
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editPrizeNameAndPicture(data=data, headers=headers):
    """
    修改中奖奖品名称与图片
    /mgmt/prmt/luckyActivity/editPrizeNameAndPicture

    参数说明:
    - modifyModule: 修改模块类型(4-中奖名称，5-中奖图片)
    - prizeId: 奖品id
    - prizeName: 奖品名称
    - prizePicture: 奖品图片
    """

    url = "/mgmt/prmt/luckyActivity/editPrizeNameAndPicture"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
