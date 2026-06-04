import os

from util.client import client

data = {
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_deleteAllMember(data=data, headers=headers):
    """
    清空导入可分享顾客
    /mgmt/prmt/share/deleteAllMember

    参数说明:
    - id: 活动主键
    - importKey: 导入操作键
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/share/deleteAllMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
