import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 产品文件
    "promotionId": 0,  # 活动id
    "serialNos": [],  # 已加入商品
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_importExchangeMain(data=data, headers=headers):
    """
    导入换购主产品
    /mgmt/prmt/importExchangeMain

    参数说明:
    - file: 产品文件
    - promotionId: 活动id
    - serialNos: 已加入商品
    """

    url = "/mgmt/prmt/importExchangeMain"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
