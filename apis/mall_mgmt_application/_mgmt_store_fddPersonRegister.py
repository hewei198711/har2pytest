import os

from util.client import client

data = {
    "certificatesNo": "",  # 身份证号码
    "memberId": 0,  # 会员ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_fddPersonRegister(data=data, headers=headers):
    """
    商城会员个人在法大大注册
    /mgmt/store/fddPersonRegister

    参数说明:
    - certificatesNo: 身份证号码
    - memberId: 会员ID
    """

    url = "/mgmt/store/fddPersonRegister"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
