import os
from urllib.parse import urlencode

from util.client import client

data = {
    "promotionId": "",  # 活动主键id
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_deleteGift(data=data, headers=headers):
    """
    详情页删除赠品池商品
    /mgmt/prmt/combine/deleteGift

    参数说明:
    - promotionId: 活动主键id
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/combine/deleteGift"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
