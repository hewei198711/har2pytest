import os

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "grantCount": 0,  # 派发数量
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "memberCard": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_addMember(data=data, headers=headers):
    """
    手动新增派发顾客
    /mgmt/prmt/couponPackage/addMember

    参数说明:
    - couponId: 优惠券id
    - grantCount: 派发数量
    - id: 活动主键
    - importKey: 导入操作键
    - memberCard: 会员卡号
    """

    url = "/mgmt/prmt/couponPackage/addMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
