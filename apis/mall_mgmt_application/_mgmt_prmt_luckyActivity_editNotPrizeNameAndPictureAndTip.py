import os

from util.client import client

data = {
    "modifyModule": 0,  # 修改模块类型(6-不中奖名称，7-不中奖图片，8-不中奖抽中提示语)
    "npId": 0,  # 不中奖奖品id
    "prizeName": "",  # 不中奖奖品名称
    "prizePicture": "",  # 不中奖奖品图片
    "tips": "",  # 不中奖提示语
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editNotPrizeNameAndPictureAndTip(data=data, headers=headers):
    """
    修改不中奖奖品名称-图片-提示语
    /mgmt/prmt/luckyActivity/editNotPrizeNameAndPictureAndTip

    参数说明:
    - modifyModule: 修改模块类型(6-不中奖名称，7-不中奖图片，8-不中奖抽中提示语)
    - npId: 不中奖奖品id
    - prizeName: 不中奖奖品名称
    - prizePicture: 不中奖奖品图片
    - tips: 不中奖提示语
    """

    url = "/mgmt/prmt/luckyActivity/editNotPrizeNameAndPictureAndTip"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
