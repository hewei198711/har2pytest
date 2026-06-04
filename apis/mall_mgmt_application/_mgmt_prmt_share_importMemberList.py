import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 顾客文件
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_share_importMemberList(data=data, headers=headers):
    """
    导入可分享顾客
    /mgmt/prmt/share/importMemberList

    参数说明:
    - file: 顾客文件
    - id: 活动主键
    - importKey: 导入操作键
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/share/importMemberList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
