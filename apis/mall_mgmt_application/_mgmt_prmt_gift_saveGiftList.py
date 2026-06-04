import os
from urllib.parse import urlencode

from util.client import client

data = {
    "importKey": "",  # importKey
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_gift_saveGiftList(data=data, headers=headers):
    """
    保存导入赠品列表
    /mgmt/prmt/gift/saveGiftList

    参数说明:
    - importKey: importKey
    """

    url = "/mgmt/prmt/gift/saveGiftList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
