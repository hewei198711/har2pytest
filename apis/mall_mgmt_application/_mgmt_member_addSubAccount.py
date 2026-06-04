import os

from util.client import client

data = {
    "memberId": 0,  # 主账号ID
    "mobile": "",  # 子账号手机号码
    "name": "",  # 名字
    "smsCode": "",  # 验证码（为空，则不通过验证码验证手机号）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_addSubAccount(data=data, headers=headers):
    """
    添加关联账号(子账号)
    /mgmt/member/addSubAccount

    参数说明:
    - memberId: 主账号ID
    - mobile: 子账号手机号码
    - name: 名字
    - smsCode: 验证码（为空，则不通过验证码验证手机号）
    """

    url = "/mgmt/member/addSubAccount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
