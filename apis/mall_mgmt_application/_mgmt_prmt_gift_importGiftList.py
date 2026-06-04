import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 顾客文件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_gift_importGiftList(data=data, headers=headers):
    """
    导入赠品列表
    /mgmt/prmt/gift/importGiftList

    参数说明:
    - file: 顾客文件
    """

    url = "/mgmt/prmt/gift/importGiftList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
