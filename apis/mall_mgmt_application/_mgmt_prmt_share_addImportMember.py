import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "mobile": "",  # 注册手机号
    "realName": "",  # 会员姓名
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_addImportMember(data=data, headers=headers):
    """
    手动添加顾客
    /mgmt/prmt/share/addImportMember

    参数说明:
    - cardNo: 会员卡号
    - id: 活动主键
    - importKey: 导入操作键
    - mobile: 注册手机号
    - realName: 会员姓名
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/share/addImportMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
