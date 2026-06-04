import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getMasterMemberInfoByCardNo(params=params, headers=headers):
    """
    根据会员卡号获取主顾客信息
    /mgmt/store/getMasterMemberInfoByCardNo

    参数说明:
    - cardNo: cardNo
    """

    url = "/mgmt/store/getMasterMemberInfoByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
