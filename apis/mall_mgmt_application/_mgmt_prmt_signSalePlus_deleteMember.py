import os

from util.client import client

data = {
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "rowId": 0,  # 行记录id
    "sourceChannel": 0,  # 操作入口:1-新增或编辑页面,2-详情页面
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_deleteMember(data=data, headers=headers):
    """
    删除活动顾客
    /mgmt/prmt/signSalePlus/deleteMember

    参数说明:
    - id: 活动主键
    - importKey: 导入操作键
    - rowId: 行记录id
    - sourceChannel: 操作入口:1-新增或编辑页面,2-详情页面
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/signSalePlus/deleteMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
