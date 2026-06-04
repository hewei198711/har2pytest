import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 产品文件
    "id": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_importProductsByDetails(data=data, headers=headers):
    """
    导入产品（详情）
    /mgmt/prmt/importProductsByDetails

    参数说明:
    - file: 产品文件
    - id: 活动id
    """

    url = "/mgmt/prmt/importProductsByDetails"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
