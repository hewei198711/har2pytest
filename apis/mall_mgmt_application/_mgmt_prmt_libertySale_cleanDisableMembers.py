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


def _mgmt_prmt_libertySale_cleanDisableMembers(data=data, headers=headers):
    """
    清空导入的不可购活动用户
    /mgmt/prmt/libertySale/cleanDisableMembers

    参数说明:
    - id: 活动主键
    - importKey: 导入操作键
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/libertySale/cleanDisableMembers"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
