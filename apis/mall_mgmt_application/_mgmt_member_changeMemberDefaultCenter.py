import os

from util.client import client

data = {
    "defaultDistributionStoreCode": "",  # 要修改成的服务中心编号
    "id": 0,  # 顾客ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_changeMemberDefaultCenter(data=data, headers=headers):
    """
    修改会员默认配送服务中心
    /mgmt/member/changeMemberDefaultCenter

    参数说明:
    - defaultDistributionStoreCode: 要修改成的服务中心编号
    - id: 顾客ID
    """

    url = "/mgmt/member/changeMemberDefaultCenter"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
