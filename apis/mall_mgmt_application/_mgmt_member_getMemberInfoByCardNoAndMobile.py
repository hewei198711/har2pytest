import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 手机号码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getMemberInfoByCardNoAndMobile(params=params, headers=headers):
    """
    根据会员卡号及手机号获取顾客信息
    /mgmt/member/getMemberInfoByCardNoAndMobile

    参数说明:
    - cardNo: 会员卡号
    - mobile: 手机号码
    """

    url = "/mgmt/member/getMemberInfoByCardNoAndMobile"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
