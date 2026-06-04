import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getMemberInfoByCardNo(params=params, headers=headers):
    """
    根据会员卡号获取顾客信息队列
    /mgmt/member/getMemberInfoByCardNo

    参数说明:
    - cardNo: 会员卡号
    """

    url = "/mgmt/member/getMemberInfoByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
