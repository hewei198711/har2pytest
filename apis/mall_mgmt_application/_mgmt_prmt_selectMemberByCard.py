import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_selectMemberByCard(params=params, headers=headers):
    """
    根据会员卡号去会员中心搜索会员信息
    /mgmt/prmt/selectMemberByCard

    参数说明:
    - cardNo: cardNo
    """

    url = "/mgmt/prmt/selectMemberByCard"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
